from datetime import datetime

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy import or_
import sqlalchemy.sql.sqltypes
from voluptuous import Schema

from .db import Database
from .models import Project, Issue, Payment, User, ProjectInvitationToken, TimeEntry, projects_users
from .auth import get_user_id

def get_table(bind, table_name: str):
    """Returns sqlalchemy core table declaration

    Args:
        bind: op.get_bind()
        table_name: str
    """

    base = automap_base()
    base.prepare(bind, reflect = True)
    return getattr(base.classes, table_name).__table__


def sqla_model_to_voluptuous(model):

    mapping = {
        sqlalchemy.sql.sqltypes.Integer: int,
        sqlalchemy.sql.sqltypes.String: str,
        sqlalchemy.sql.sqltypes.DateTime: str,
    }

    schema_dict = {}

    for prop in class_mapper(model).iterate_properties:
        if not isinstance(prop, ColumnProperty):
            continue
        schema_dict[prop.key] = mapping[type(prop.columns[0].type)]

    return Schema(schema_dict, required = False)


def entry_stat_from_list(time_entries):
    stat = {
        'spent': 0,
        'last_entry': 0,
        'count': len(time_entries),
    }
    for entry in time_entries:
        if entry.end and entry.end.timestamp() > stat['last_entry']:
            stat['last_entry'] = entry.end.timestamp()
        if entry.start.timestamp() > stat['last_entry']:
            stat['last_entry'] = entry.start.timestamp()
        stat['spent'] += ((entry.end or datetime.now()) - entry.start).total_seconds()
    return stat

def project_to_dict(project: Project):
    paid = 0
    for payment in project.payments:
        paid += payment.amount
    return {
        'id': project.id,
        'name': project.name,
        'desc': project.desc,
        'time_stat': entry_stat_from_list(project.time_entries),
        'issues': [i.id for i in project.issues],
        'paid': paid,
        'users': [u.id for u in project.users],
        'payments': [p.id for p in project.payments],
        'tokens': [t.id for t in project.tokens],
    }

def issue_to_dict(issue: Issue):
    return {
        'id': issue.id,
        'name': issue.name,
        'desc': issue.desc,
        'status': issue.status,
        'rank': issue.rank,
        'project_id': issue.project_id,
        'reporter_id': issue.reporter_id,
        'assignee_id': issue.assignee_id,
        'time_stat': entry_stat_from_list(issue.time_entries),
        'time_entries': [t.id for t in issue.time_entries],
        'status_date': issue.status_date.timestamp(),
    }

def payment_to_dict(payment: Payment):
    return {
        'id': payment.id,
        'project_id': payment.project_id,
        'created_user_id': payment.created_user_id,
        'paid_user_id': payment.paid_user_id,
        'amount': payment.amount,
        'time': payment.time.timestamp(),
        'note': payment.note,
    }

def user_to_dict(user: User):
    return {
        'id': user.id,
        'name': user.name,
        'avatar': user.avatar,
    }

def project_token_to_dict(prj_token: ProjectInvitationToken):
    return {
        'id': prj_token.id,
        'token': prj_token.token,
        'project_id': prj_token.project_id,
    }

def time_entry_to_dict(time_entry: TimeEntry):
    return {
        'id': time_entry.id,
        'issueId': time_entry.issue_id,
        'project_id': time_entry.project_id,
        'userId': time_entry.user_id,
        'start': time_entry.start.timestamp(),
        'end': time_entry.end.timestamp() if time_entry.end else None,
    }


def idize(func, rows: list) -> dict:
    return {r.id: func(r) for r in rows}

def get_all_project_data(db: Database, project_id = None):
    user_id = get_user_id()
    with db.session_scope() as conn:
        project_query = conn.query(Project).join(projects_users).join(User).filter(User.id == user_id)
        if project_id:
            project_query = project_query.filter(Project.id == project_id)
        project_rows = project_query.all()
        project_id_list = [r.id for r in project_rows]

        project_user_rows = conn.query(User).join(projects_users).join(Project).filter(Project.id.in_(project_id_list)).all()
        users = idize(user_to_dict, project_user_rows)

        # if somebody left the project still needs his/her data
        issue_users = [i.assignee_id for i in conn.query(Issue.assignee_id).filter(~Issue.assignee_id.in_(users.keys())).all()]
        issue_users += [i.reporter_id for i in conn.query(Issue.reporter_id).filter(~Issue.reporter_id.in_(users.keys())).all()]

        if issue_users:
            users.update(idize(user_to_dict, conn.query(User).filter(User.id.in_(issue_users))))

        return {
            'projects': idize(project_to_dict, project_rows),
            'issues': idize(issue_to_dict, conn.query(Issue).filter(Issue.project_id.in_(project_id_list)).all()),
            'time_entries': idize(time_entry_to_dict, conn.query(TimeEntry).filter(TimeEntry.project_id.in_(project_id_list)).all()),
            'users': users,
            'payments': idize(payment_to_dict, conn.query(Payment).filter(Payment.project_id.in_(project_id_list)).all()),
            'project_invitation_tokens': idize(project_token_to_dict, conn.query(ProjectInvitationToken).filter(ProjectInvitationToken.project_id.in_(project_id_list)).all()),
        }
