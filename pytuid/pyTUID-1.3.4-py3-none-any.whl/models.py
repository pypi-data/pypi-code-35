import ast
from django.db import models
from django.utils.translation import ugettext as _


class TUIDUser(models.Model):
    """Represents a TUID user with various properties returned from CAS"""
    class Meta:
        verbose_name = _('TUID User')
        verbose_name_plural = _('TUID Users')

    uid = models.CharField(max_length=50, unique=True, verbose_name=_('TUID'))
    surname = models.CharField(max_length=50, verbose_name=_('surname'))
    given_name = models.CharField(max_length=50, verbose_name=_('given name'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    groups = models.TextField(verbose_name=_('cas groups'))

    def group_list(self):
        """Returns all the groups as list of strings"""
        if self.groups and len(self.groups) > 0:
            return ast.literal_eval(self.groups) if self.groups[0] == '[' and self.groups[-1] == ']' else [self.groups]
        else:
            return []

    def in_group(self, group_string):
        """Checks wether this user is in the specified group"""
        return group_string in self.group_list()

    def name(self):
        """Returns the users full name"""
        return self.given_name + ' ' + self.surname
    name.short_description = _('name')

    def __str__(self):
        return self.name() + ' (' + self.uid + ')'
