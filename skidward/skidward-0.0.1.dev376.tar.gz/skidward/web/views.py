from flask import request, redirect, url_for, flash
from flask_admin.menu import MenuLink
from wtforms import validators
from wtforms.fields import PasswordField
from wtforms.fields.html5 import EmailField
from flask_admin.form import fields
from flask_admin.model.template import EndpointLinkRowAction
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_security import login_required, current_user, utils, logout_user, login_user

from skidward.models import db, Task
from skidward.backend import RedisBackend
from skidward.web.forms import TaskContextForm


class SkidwardModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("index.login"))


class UserAdmin(SkidwardModelView):
    form_excluded_columns = ("password",)
    column_exclude_list = ("password",)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.email = EmailField(
            "Email ID", [validators.DataRequired(), validators.Email()]
        )
        form_class.new_password = PasswordField("New Password")
        form_class.confirm_password = PasswordField(
            "Confirm Password",
            [validators.EqualTo("new_password", message="Passwords do not match")],
        )
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.new_password):
            model.password = utils.hash_password(model.new_password)


class RoleAdmin(SkidwardModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")


class WorkerView(SkidwardModelView):
    can_create = False


class TaskView(SkidwardModelView):

    column_extra_row_actions = [
        EndpointLinkRowAction(
            icon_class="glyphicon glyphicon-cog",
            endpoint="add_context.add_context",
            title="Configure",
            id_arg="task_id",
        ),
        EndpointLinkRowAction(
            icon_class="glyphicon glyphicon-play-circle",
            endpoint="add_context.add_context",
            title="Configured_Run",
            id_arg="task_id",
            url_args=dict(temp_run=True),
        ),
        EndpointLinkRowAction(
            icon_class="glyphicon glyphicon-play",
            endpoint="run_task.run_task",
            title="Quick_Run",
            id_arg="task_id",
        ),
    ]

    form_overrides = {"context": fields.JSONField}
    form_excluded_columns = ("context",)
    form_create_rules = ("name", "cron_string", "worker")


class JobView(SkidwardModelView):

    column_list = ["task", "ran_at", "state"]
    column_labels = dict(task="Jobs", state="Status")


class SkidwardView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("index.login"))

    def is_visible(self):
        return False

    @login_required
    @expose("/")
    def index(self):
        return self.render("admin/index.html")

    @expose("/login")
    def login(self):
        login_user(current_user)
        return redirect(url_for("admin.index"))

    @expose("/logout")
    def logout(self):
        logout_user()
        return redirect(url_for("index.login"))


class RunView(SkidwardView):
    @expose("/run/<task_id>")
    @login_required
    def run_task(self, task_id):
        task = Task.query.get(task_id)
        context = request.args.get("context")

        if not context and not task.context:
            flash("Cannot Run Task without Configuration.", category="error")
            return redirect(url_for("add_context.add_context", task_id=task_id))

        redis_client = RedisBackend()
        if context:
            temp_task = {"task_id": task_id, "overwrite_context": context}
            redis_client.hmset("CONFIGURED_RUN", temp_task)
            flash("Job is Running... Refresh the page to view updated Status")
            return redirect("/admin/job")

        else:
            redis_client.lpush("MANUAL_RUN", task_id)
            flash("Job is Running... Refresh the page to view updated Status")
            return redirect("/admin/job")


class TaskConfigure(SkidwardView):
    @expose("/configure/<task_id>", methods=["GET", "POST"])
    @login_required
    def add_context(self, task_id):
        form = TaskContextForm()
        task = Task.query.get(task_id)

        if task.context:
            form.context.data = task.context

        if form.validate_on_submit():
            dict_of_fieldlist = request.form.to_dict(flat=False)
            keys = dict_of_fieldlist["key"]
            values = dict_of_fieldlist["value"]
            context = dict(zip(keys, values))

            if request.args.get("temp_run"):
                return redirect(
                    url_for("run_task.run_task", task_id=task.id, context=context)
                )

            else:
                task.context = context
                db.session.commit()
                return redirect(url_for("add_context.index"))

        return self.render("task/configure.html", form=form, name=task.name)


class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
