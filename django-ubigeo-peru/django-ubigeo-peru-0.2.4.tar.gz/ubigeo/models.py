# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import ValidationError


class Ubigeo(models.Model):

    REGION = 1
    PROVINCE = 2
    DISTRICT = 3

    POLITICAL_DIVISION_CHOICES = (
        (REGION, "Region"),
        (PROVINCE, "Provincia"),
        (DISTRICT, "Distrito")
    )

    parent = models.ForeignKey('Ubigeo', null=True)
    name = models.TextField()
    reniec_code = models.CharField(max_length=6)
    political_division = models.PositiveSmallIntegerField(
        choices=POLITICAL_DIVISION_CHOICES
    )

    def __repr__(self):
        return self.qualified_name(self)

    def __str__(self):
        return '{} - {}'.format(self.parent if self.parent else '', self.name)

    @property
    def human_political_division(self,):
        if self.political_division == 1:
            return u"Region"
        elif self.political_division == 2:
            return u"Provincia"
        elif self.political_division == 3:
            return u"Distrito"
        elif self.political_division == 4:
            return u"Internacional"
        else:
            return u"No sé"

    @staticmethod
    def qualified_name(ubigeo):
        """
        ie. Distrito de Magdalena en la provicina de Lima en la region de Lima
        """
        if ubigeo.parent is None:
            return u"{} de {}".format(
                ubigeo.human_political_division, ubigeo.name
            )
        else:
            return u"{} de {} en la {}".format(
                ubigeo.human_political_division,
                ubigeo.name,
                Ubigeo.qualified_name(ubigeo.parent)
            )

    def __eq__(self, other):
        """
        Comparar name con name y parents
        """
        if not other:
            return False
        elif self.name != other.name:
            return False
        elif (self.parent is None and other.parent is not None) or \
             (self.parent is not None and other.parent is None):
            return False
        elif self.parent is None:
            return True
        else:
            return self.parent == other.parent

    @staticmethod
    def guess_political_division_from_code(code):
        if code.pk[0:2] == "00":
            return "No idea'"
        elif code.pk[2:4] == "00":
            return "Region"
        elif code.pk[4:6] == "00":
            return "Provincia"
        else:
            return "Distrito"

    @staticmethod
    def get_ubigeo_map(ubigeo=None, map_ubigeo={}):
        if ubigeo:
            map_ubigeo[ubigeo.human_political_division.lower()] = ubigeo.name
            if ubigeo.parent:
                Ubigeo.get_ubigeo_map(ubigeo.parent, map_ubigeo)

            map_ubigeo['id'] = ubigeo.id

        return map_ubigeo

    def clean(self):
        """
        Don't allow null parent except when political_divison is Region
        """
        if self.parent is None and self.political_divison != 1:
            raise ValidationError("Only Regions can have no parent.")
