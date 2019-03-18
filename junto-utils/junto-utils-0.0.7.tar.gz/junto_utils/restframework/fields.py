from collections import OrderedDict
from datetime import datetime, timedelta

from django.utils.timezone import get_fixed_timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from rest_framework import serializers


class PrimaryKeyRelatedNestedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, serializer_class=None, **kwargs):
        assert serializer_class, 'you should pass serializer class'
        self.serializer_class = serializer_class
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.serializer_class(value, context=self.context).data

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                getattr(item, 'pk'),
                self.display_value(item)
            )
            for item in queryset
        ])


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        password_validation.validate_password(password=data)
        return data


class SlugRelatedCreationAbsenceField(serializers.SlugRelatedField):
    """
    Аналог SlugRelatedField с отличием в том, что те, объекты, которые не нашлись по slug_field, создадутся

    Модель, переданного queryset должна содержать только 1 обязательное поле,
    которое совпадает с переданным slug_field,
    иначе объект модели не получится создать по одному лишь slug_field и будет ошибка
    # ToDo: можно придумать оптимизации для many=True случаев, чтобы уменьшить кол-во запросов
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail('invalid')


class WeekDayField(serializers.ChoiceField):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'

    WEEKDAY_CHOICES = (
        (MONDAY, 'MONDAY'),
        (TUESDAY, 'TUESDAY'),
        (WEDNESDAY, 'WEDNESDAY'),
        (THURSDAY, 'THURSDAY'),
        (FRIDAY, 'FRIDAY'),
        (SATURDAY, 'SATURDAY'),
        (SUNDAY, 'SUNDAY'),
    )

    WEEKDAYS = {
        MONDAY: 0,
        TUESDAY: 1,
        WEDNESDAY: 2,
        THURSDAY: 3,
        FRIDAY: 4,
        SATURDAY: 5,
        SUNDAY: 6,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(choices=self.WEEKDAY_CHOICES, *args, **kwargs)

    def to_internal_value(self, data):
        weekday = super().to_internal_value(data)
        # Перобразуем строковое представление дня недели в джанговский номер
        return self.WEEKDAYS[weekday]

    def to_representation(self, value):
        python_weekdays_to_weekday_name = {v: k for k, v in self.WEEKDAYS.items()}
        return python_weekdays_to_weekday_name[value]


class TimezoneField(serializers.CharField):
    def to_internal_value(self, time_zone):
        if str(time_zone)[0] not in ['-', '+']:
            raise serializers.ValidationError(
                _('Timezone has wrong format. Use one of these formats instead: +HH:MM|-HH:MM')
            )
        try:
            time_diff = datetime.strptime(time_zone[1:], '%H:%M')
            time_delta = timedelta(hours=time_diff.hour, minutes=time_diff.minute)
        except ValueError:
            raise serializers.ValidationError(
                _('Timezone has wrong format. Use one of these formats instead: +HH:MM|-HH:MM')
            )
        if time_zone[0] == '-':
            time_delta = -time_delta
        return get_fixed_timezone(time_delta)

