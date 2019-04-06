import logging
import random
import string
from datetime import datetime, timedelta
from functools import partial

from dateutil.parser import parse as dateparser
from flask import Flask, abort, request
from jsonrpc.backend.flask import JSONRPCAPI
from pytimeparse import parse
from voluptuous import Schema

from pabu.auth import get_user_id, is_logged_in
from pabu.db import Database
from pabu.models import Issue, Payment, Project, ProjectInvitationToken, TimeEntry, User, projects_users
from pabu.tools import (entry_stat_from_list, issue_to_dict, project_to_dict, project_token_to_dict, sqla_model_to_voluptuous,
                        time_entry_to_dict, user_to_dict, payment_to_dict, get_all_project_data as get_all_project_data_)

logger = logging.getLogger(__name__)

def random_str(len: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len))

def add_api_controllers(app: Flask, db: Database):

    jsonrpc_api = JSONRPCAPI()

    app.add_url_rule('/', 'api', jsonrpc_api.as_view(), methods=['POST'])

    def get_current_user(conn):
        user_id = get_user_id()
        return conn.query(User).filter(User.id == user_id).first()

    @app.before_request
    def check_login(): # pylint: disable=unused-variable
        if not is_logged_in():
            abort(401)

    @app.before_request
    def common_log(): # pylint: disable=unused-variable
        logger.info("JSONRPC method '%s' called with args: %s" % (request.json['method'], request.json['params']))
        request.start = datetime.now()

    @app.after_request
    def print_time(response): # pylint: disable=unused-variable
        logger.info("JSONRPC method '%s' responded in %s ms", request.json['method'], (datetime.now() - request.start).total_seconds()*1000)
        return response

    def check_project(project_id, conn):
        user_id = get_user_id()
        if conn.query(Project).join(projects_users).join(User).filter(User.id == user_id).filter(Project.id == project_id).count() != 1:
            logger.error("check_project failed! project: %s, user: %s", project_id, user_id)
            abort(404)

    @jsonrpc_api.dispatcher.add_method
    def create_project(name: str, desc: str): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            prj = Project(name = name, desc = desc, users = [get_current_user(conn)])
            conn.add(prj)
            conn.flush()
            return project_to_dict(prj)

    @jsonrpc_api.dispatcher.add_method
    def update_project(id: int, name: str, desc: str): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(id, conn)
            project = conn.query(Project).filter(Project.id == id).first() # type: Project
            project.name = name
            project.desc = desc
            return project_to_dict(project)

    @jsonrpc_api.dispatcher.add_method
    def get_projects(id: int = None): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            qs = conn.query(Project).outerjoin(Payment).join(projects_users).join(User).filter(User.id == user_id) \
                     .outerjoin(Issue,Project.id == Issue.project_id)
            if id:
                qs = qs.filter(Project.id == id)
            data = {r.id: project_to_dict(r) for r in qs.all()}
        return data

    def process_resources(raw_data_list: list, model, conn, handler):
        schema = sqla_model_to_voluptuous(model)
        res = []

        for raw_data in raw_data_list:

            if 'id' in raw_data and raw_data['id'] is None:
                del raw_data['id']

            data = schema(raw_data)

            if 'pre_process' in handler:
                data.update(handler['pre_process'](data))

            if 'id' in data:
                instance = conn.query(model).filter(model.id == data['id']).first()
                if not instance:
                    abort(404)
                handler['checker'](instance)
                if 'pre_update' in handler:
                    handler['pre_update'](data, instance)
                for key, value in data.items():
                    setattr(instance, key, value)
            else:
                instance = model(**data)
                handler['checker'](instance)
                conn.add(instance)

            conn.flush()

            if 'post_process' in handler:
                new_data = handler['post_process'](data, instance)
                if new_data:
                    for key, value in new_data.items():
                        setattr(instance, key, value)
                    conn.flush()

            res.append(instance)

        return res

    @jsonrpc_api.dispatcher.add_method
    def process_issues(issues): # pylint: disable=unused-variable
        def pre_update(new_data: dict, old_issue: Issue):
            if 'status' in new_data and old_issue.status != new_data['status']:
                new_data['status_date'] = datetime.now()
                if new_data['status'] == 'in progress':
                    new_data['assignee_id'] = get_user_id()
                if new_data['status'] == 'todo':
                    new_data['assignee_id'] = None

        with db.session_scope() as conn:
            issues = process_resources(issues, Issue, conn, {
                'pre_process': lambda d: {'reporter_id': get_user_id()},
                'pre_update': pre_update,
                'checker': lambda i: check_project(i.project_id, conn),
                'post_process': lambda d, i: None if 'id' in d else {'rank': i.id},
            })
            return {i.id: issue_to_dict(i) for i in issues}

    @jsonrpc_api.dispatcher.add_method
    def get_issues(project_id: int): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            rows = conn.query(Issue).join(Project).join(projects_users).join(User).filter(User.id == user_id) \
                       .filter(Project.id == project_id).all()
            return {r.id: issue_to_dict(r) for r in rows}

    @jsonrpc_api.dispatcher.add_method
    def get_time_entries(project_id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(project_id, conn)
            rows = conn.query(TimeEntry).filter(Project.id == project_id).all()
            return {r.id: time_entry_to_dict(r) for r in rows}

    @jsonrpc_api.dispatcher.add_method
    def add_time(project_id: int, amount: str, start: str, issue_id = None): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            check_project(project_id, conn)
            seconds = parse(amount)
            start = dateparser(start) if start else (datetime.now() - timedelta(seconds = seconds))
            end = start + timedelta(seconds = seconds)
            entry = TimeEntry(project_id = project_id, issue_id = issue_id, start = start, end = end, user_id = user_id)
            conn.add(entry)

    @jsonrpc_api.dispatcher.add_method
    def start_time(project_id, issue_id = None): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            check_project(project_id, conn)
            entry = TimeEntry(project_id = project_id, issue_id = issue_id, user_id = user_id)
            conn.add(entry)

    @jsonrpc_api.dispatcher.add_method
    def stop_time(): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            entry = conn.query(TimeEntry).filter(TimeEntry.user_id == user_id).filter(TimeEntry.end.is_(None)).first()
            if entry:
                entry.end = datetime.now()
                return time_entry_to_dict(entry)

    @jsonrpc_api.dispatcher.add_method
    def get_ticking_stat(): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            entry = conn.query(TimeEntry).filter(TimeEntry.user_id == user_id, TimeEntry.end.is_(None)).first()
            if entry:
                return {'ticking': True, 'entry': time_entry_to_dict(entry)}
            else:
                return {'ticking': False}
        return {}

    @jsonrpc_api.dispatcher.add_method
    def get_payments(project_id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(project_id, conn)
            rows = conn.query(Payment).filter(Payment.project_id == project_id).all()
            return {r.id:payment_to_dict(r) for r in rows}

    @jsonrpc_api.dispatcher.add_method
    def add_payment(project_id: int, amount: str, paid_user_id: int, time: str, note: str): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            check_project(project_id, conn)
            payment = Payment(project_id = project_id, amount = parse(amount), paid_user_id = paid_user_id, created_user_id = user_id,
                              note = note, time = dateparser(time) if time else datetime.now())
            conn.add(payment)
            return True

    @jsonrpc_api.dispatcher.add_method
    def get_project_users(project_id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(project_id, conn)
            rows = conn.query(User).join(projects_users).join(Project).filter(Project.id == project_id).all()
            return {r.id: user_to_dict(r) for r in rows}

    @jsonrpc_api.dispatcher.add_method
    def delete_project(id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(id, conn)
            conn.query(Project).filter(Project.id == id).delete()
            return True

    @jsonrpc_api.dispatcher.add_method
    def delete_issue(id: int): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            issue = conn.query(Issue).join(Project).join(projects_users).join(User).filter(User.id == user_id).filter(Issue.id == id).first()
            if not issue:
                abort(404)
            conn.delete(issue)
            return True

    @jsonrpc_api.dispatcher.add_method
    def delete_time_entry(id: int): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            qs = conn.query(TimeEntry).join(Project).join(projects_users).join(User).filter(User.id == user_id).filter(TimeEntry.id == id)
            entry = qs.first()
            if not entry:
                abort(404)
            conn.delete(entry)
            return True

    @jsonrpc_api.dispatcher.add_method
    def delete_payment(id: int): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            qs = conn.query(Payment).join(Project).join(projects_users).join(User).filter(User.id == user_id).filter(Payment.id == id)
            payment = qs.first()
            if not payment:
                abort(404)
            conn.delete(payment)
            return True

    @jsonrpc_api.dispatcher.add_method
    def create_project_token(id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            proj_token = ProjectInvitationToken(project_id = id, token = random_str(32))
            conn.add(proj_token)
            conn.flush()
            return project_token_to_dict(proj_token)

    @jsonrpc_api.dispatcher.add_method
    def delete_project_token(id: int): # pylint: disable=unused-variable
        user_id = get_user_id()
        with db.session_scope() as conn:
            qs = conn.query(ProjectInvitationToken).join(Project).join(projects_users).join(User).filter(User.id == user_id) \
                      .filter(ProjectInvitationToken.id == id)
            prj_token = qs.first()
            if not prj_token:
                abort(404)
            conn.delete(prj_token)
            return True

    @jsonrpc_api.dispatcher.add_method
    def get_project_tokens(id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(id, conn)
            rows = conn.query(ProjectInvitationToken).filter(ProjectInvitationToken.project_id == id).all()
            return {r.id: project_token_to_dict(r) for r in rows}

    @jsonrpc_api.dispatcher.add_method
    def join_to_project(token: str): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            user_id = get_user_id()
            prj_token = conn.query(ProjectInvitationToken).filter(ProjectInvitationToken.token == token).first()
            if not prj_token:
                abort(404)
            project = conn.query(Project).filter(Project.id == prj_token.project_id).first() # type: Project
            user = conn.query(User).filter(User.id == user_id).first()
            if user not in project.users:
                project.users.append(user)
            return True

    @jsonrpc_api.dispatcher.add_method
    def kick_user_from_project(project_id: int, user_id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(project_id, conn)
            project = conn.query(Project).filter(Project.id == project_id).first() # type: Project
            user = conn.query(User).filter(User.id == user_id).first()
            project.users.remove(user)
            return True

    @jsonrpc_api.dispatcher.add_method
    def leave_project(project_id: int): # pylint: disable=unused-variable
        with db.session_scope() as conn:
            check_project(project_id, conn)
            user_id = get_user_id()
            project = conn.query(Project).filter(Project.id == project_id).first() # type: Project
            user = conn.query(User).filter(User.id == user_id).first()
            project.users.remove(user)
            return True


    @jsonrpc_api.dispatcher.add_method
    def get_all_project_data(id: int): # pylint: disable=unused-variable
        return get_all_project_data_(db, id)

    @jsonrpc_api.dispatcher.add_method
    def ping(): # pylint: disable=unused-variable
        return 1/0
