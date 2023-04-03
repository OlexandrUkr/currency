from django.db import models
from django.templatetags.static import static

from currency.choices import RateCurrencyChoices


def source_path(instance, filename):
    return f"sources/{instance.name}/{filename}"


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    currency = models.PositiveSmallIntegerField(
        choices=RateCurrencyChoices.choices,
        default=RateCurrencyChoices.USD
    )
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE)

    def __str__(self):
        return f'Currency: {self.get_currency_display()}'


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    email_from = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

    def __str__(self):
        return f'Email from: {self.email_from}'


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    note = models.CharField(max_length=255, null=True, blank=True)
    source_logo = models.FileField(
        default=None,
        null=True,
        blank=True,
        upload_to=source_path
    )

    def __str__(self):
        return self.name

    @property
    def source_logo_url(self):
        if self.source_logo:
            return self.source_logo.url

        return static('no-image.png')


class RequestResponseLog(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    time = models.DecimalField(max_digits=30, decimal_places=20)
