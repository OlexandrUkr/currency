import random

from django.core.management.base import BaseCommand
from currency.models import Rate, Source
from currency.choices import RateCurrencyChoices


class Command(BaseCommand):
    # help = "Generate random test rates"

    def handle(self, *args, **options):
        source, _ = Source.objects.get_or_create(code_name='1', defaults={'name': 1})

        for _ in range(400):
            Rate.objects.create(
                buy=random.randint(30, 40),
                sale=random.randint(30, 40),
                currency=random.choices(RateCurrencyChoices.choices)[0][0],
                source=source
            )
