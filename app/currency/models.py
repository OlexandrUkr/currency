from django.db import models

from currency.choices import RateCurrencyChoices


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    currency = models.PositiveSmallIntegerField(
        choices=RateCurrencyChoices.choices,
        default=RateCurrencyChoices.USD
    )
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    source = models.CharField(max_length=25)

    def __str__(self):
        return f'Currency: {self.get_currency_display()}'


class ContactUs(models.Model):
    email_from = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

    def __str__(self):
        return f'Email from: {self.email_from}'


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Source url: {self.source_url}'
