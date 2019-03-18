import factory
from .models import Profile
from djangoldp.factories import UserFactory
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    available = factory.Faker('null_boolean')
    bio = factory.Faker('text', max_nb_chars=250)
    city = factory.Faker('city')
    country = factory.Faker('country')
    phone = factory.Faker('phone_number')
    website = factory.Faker('url')
