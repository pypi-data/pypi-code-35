from django.db import models
from django.conf import settings

from .helpers import SimpleUserFeedback


class UserGenericTypeformFeedbackManager(models.Manager):

    def build_simple_user_feedback(self, user_from, step_stream):
        url = None
        object_id = None
        status = settings.RATINGS_USER_FEEDBACK_STATUS_NONE
        user_feedback = None
        team = user_from.teams.filter_by_project(step_stream.step.project).filter(stream=step_stream.stream).first()
        if not team:
            return None
        members = team.members
        team_member = members.get_by_user(user_from)
        user_feedback, _ = team_member.get_or_create_feedback_for_step(step_stream.step)
        if not user_feedback:
            return None
        url = user_feedback.feedback.typeform_url
        status = user_feedback.status
        object_id = user_feedback.pk
        return SimpleUserFeedback(
            id=object_id,
            url=url,
            status=status,
            user_object=user_feedback,
        )
