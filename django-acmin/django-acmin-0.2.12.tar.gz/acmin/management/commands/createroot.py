from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from acmin.models import Group, User, GroupPermission, SuperPermissionModel, ContentType
        group = Group.objects.update_or_create(name="root")[0]

        user = User.objects.filter(username="root").first()
        if not user:
            user = User(group=group, username="root", title="root")
            user.set_password("123456")
            user.save()

        contenttype = ContentType.objects.filter(name=SuperPermissionModel.__name__).first()
        permission = GroupPermission.objects.filter(group=group, contenttype=contenttype).first()
        if not permission:
            GroupPermission.objects.create(
                group=group,
                contenttype=contenttype,
                name="root",
                creatable=True,
                savable=True,
                removable=True,
                cloneable=True,
                exportable=True,
                viewable=True,
                listable=True,
            )
