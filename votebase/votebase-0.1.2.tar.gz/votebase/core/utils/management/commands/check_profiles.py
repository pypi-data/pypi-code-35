from progressbar import ProgressBar, Percentage, Bar

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from votehub.apps.accounts.models import Profile
from votehub.apps.utils.common import generate_token, generate_slug_for_user

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()
        total = users.count()
        progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=int(total)).start()
        updated = 0
        i = 0

        for user in users:
            progress_bar.update(i + 1)
            try:
                profile = user.get_profile()
                if len(profile.token) is 0:
                    profile.token = generate_token(user)
                    profile.save()
                    updated += 1
                if len(profile.token) is 0:
                    profile.token = generate_slug_for_user(
                        first_name=user.first_name,
                        last_name=user.last_name,
                    ),
                    profile.save()
                    updated += 1
            except ObjectDoesNotExist:
                profile = Profile.objects.create(
                    user=user,
                    slug=generate_slug_for_user(
                        first_name=user.first_name,
                        last_name=user.last_name,
                    ),
                    token=generate_token(user)
                )
                profile.save()
                updated += 1

            i += 1

        self.stdout.write('Successfully updated %(updated)i profiles from %(total)i users.' % {
            'total': total,
            'updated': updated,
        })

        progress_bar.finish()