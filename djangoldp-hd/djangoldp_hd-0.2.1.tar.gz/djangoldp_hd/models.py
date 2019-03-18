from django.contrib.auth.models import User, Group

User._meta.serializer_fields = ['@id', 'account', 'username', 'chatProfile', 'first_name', 'last_name', 'email', 'groups', 'profile', 'skills']
Group._meta.serializer_fields = ['name']