from collections import defaultdict
from copy import deepcopy
from django.apps import apps
from django.db import models


class DatabaseReference(object):
    def __init__(self, model, pk):
        self.model = model
        self.pk = pk

    def __repr__(self):
        return '<%s %s>' % (self.model, self.pk)

    def get(self):
        model = apps.get_model(*self.model.split('.'))
        return model.objects.get(pk=self.pk)


class DatabaseContext(object):
    class ObjectNotFound(Exception):
        pass

    class SpecError(Exception):
        pass

    def __init__(self):
        self.__log = {
            'created': [],
            'updated': [],
            'deleted': []
        }

    def get_model(self, name):
        return apps.get_model(*name.split('.'))

    def __update(self, obj, data):
        opts = obj._meta
        m2ms = defaultdict(list)

        for key, value in data.items():
            field = opts.get_field(key)
            if isinstance(field, models.ForeignKey):
                if not isinstance(value, DatabaseReference):
                    raise self.SpecError(
                        '%s must be a DatabaseReference, not %s' % (
                            field,
                            type(value)
                        )
                    )

                setattr(obj, key, value.get())
            elif isinstance(field, models.ManyToManyField):
                if isinstance(value, (list, tuple)):
                    m2ms[key].extend(value)
                else:
                    m2ms[key].append(value)
            else:
                setattr(obj, key, value)

        obj.save()

        for field, values in m2ms.items():
            subs = getattr(obj, field)
            added = []

            for i, value in enumerate(values):
                if not isinstance(value, DatabaseReference):
                    raise self.SpecError(
                        '%s[%d] must be a DatabaseReference, not %s' % (
                            field,
                            i,
                            type(value)
                        )
                    )

                subobj = value.get()
                subs.add(subobj)
                added.append(subobj.pk)

            subs.remove(*subs.exclude(pk__in=added))

    def create(self, model, data, update_on=None):
        Model = self.get_model(model)
        created = False

        if update_on:
            try:
                obj = Model.objects.get(
                    **{
                        update_on: data[update_on]
                    }
                )
            except Model.DoesNotExist:
                obj = Model()
                created = True
        else:
            obj = Model()
            created = True

        self.__update(obj, data)
        self.__log[created and 'created' or 'updated'].append(
            (
                model,
                obj.pk
            )
        )

        return DatabaseReference(
            model,
            obj.pk
        )

    def update(self, model, data, **filter):
        Model = self.get_model(model)
        updates = []

        for obj in Model.objects.filter(**filter):
            self.__update(obj, data)
            updates.append(
                (
                    model,
                    obj.pk
                )
            )

        self.__log['updated'].extend(updates)

        return [
            DatabaseReference(*o)
            for o in updates
        ]

    def delete(self, model, **filter):
        Model = self.get_model(model)
        deletes = []

        for obj in Model.objects.filter(**filter):
            obj.delete()
            deletes.append(
                (
                    model,
                    obj.pk
                )
            )

        self.__log['deleted'].extend(deletes)
        return [
            DatabaseReference(*o)
            for o in deletes
        ]

    def ref(self, model, **filter):
        Model = self.get_model(model)

        for obj in Model.objects.filter(**filter):
            return DatabaseReference(model, obj.pk)

        raise self.ObjectNotFound(
            '%s object matching filter expression not found' % model
        )

    def __transform(self, obj):
        d = {}

        opts = obj._meta
        for field in opts.get_fields():
            if isinstance(
                field,
                (
                    models.AutoField,
                    models.BooleanField,
                    models.CharField,
                    models.DateField,
                    models.DecimalField,
                    models.IntegerField,
                    models.TextField
                )
            ):
                d[field.name] = getattr(obj, field.name)
            elif isinstance(
                field,
                (
                    models.ManyToOneRel,
                    models.ManyToManyField
                )
            ):
                continue
            elif isinstance(field, models.ForeignKey):
                rm = field.related_model
                v = getattr(obj, '%s_id' % field.name)

                d[field.name] = v and DatabaseReference(
                    '%s.%s' % (
                        rm._meta.app_label,
                        rm._meta.model_name
                    ),
                    v
                ) or None

        return d

    def get(self, model, **filter):
        Model = self.get_model(model)
        yielded = False

        for obj in Model.objects.filter(**filter):
            yield self.__transform(obj)
            yielded = True

        if not yielded:
            raise self.ObjectNotFound(
                '%s object matching filter expression not found' % model
            )

    def latest(self, model, **filter):
        Model = self.get_model(model)

        try:
            obj = Model.objects.filter(**filter).latest()
        except Model.DoesNotExist:
            raise self.ObjectNotFound(
                '%s object matching filter expression not found' % model
            )
        else:
            return self.__transform(obj)

    def log(self):
        return deepcopy(self.__log)
