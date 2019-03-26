from django.conf import settings
from django.core.management.base import BaseCommand

from capitalist import Capitalist
from ...models import Account, Currency


class Command(BaseCommand):
    def handle(self, *args, **options):
        cap = Capitalist(settings.CAPITALIST_LOGIN, settings.CAPITALIST_PASSWORD)

        for acc in cap.accounts():
            Account.objects.update_or_create(number=acc.number, defaults={
                'balance': acc.balance,
                'blocked_amount': acc.blocked_amount,
                'currency': Currency.objects.get_or_create(code=acc.currency)[0],
                'name': acc.name,
                'number': acc.number,
            })

        self.stdout.write(self.style.SUCCESS('Accounts updated successfully'))
