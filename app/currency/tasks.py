from celery import shared_task
from django.conf import settings
from currency.choices import RateCurrencyChoices
import requests
from bs4 import BeautifulSoup

from currency.constants import PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME, FINANCE_UA_CODE_NAME
from currency.utils import to_2_places_decimal


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source
    # source = Source.objects.filter(code_name=PRIVATBANK_CODE_NAME).first()
    #
    # if source is None:
    #     source = Source.objects.create(code_name=PRIVATBANK_CODE_NAME, name='PrivatBank')
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    source, _ = Source.objects.get_or_create(
        code_name=PRIVATBANK_CODE_NAME,
        defaults={
            'source_url': url,
            'name': 'PrivatBank'
        }
    )

    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()

    available_currency = {
        'USD': RateCurrencyChoices.USD,
        'EUR': RateCurrencyChoices.EUR,
    }

    for rate in rates:
        if rate['ccy'] not in available_currency:
            continue

        buy = to_2_places_decimal(rate['buy'])
        sale = to_2_places_decimal(rate['sale'])
        currency = rate['ccy']

        last_rate = Rate.objects.filter(
            currency=available_currency[currency],
            source=source
        ) \
            .order_by('-created') \
            .first()

        if hasattr(last_rate, 'pk'):
            if last_rate.buy != buy or last_rate.sale != sale:
                Rate.objects.create(
                    buy=buy,
                    sale=sale,
                    currency=available_currency[currency],
                    source=source
                )
        else:
            Rate.objects.create(
                buy=buy,
                sale=sale,
                currency=available_currency[currency],
                source=source
            )


@shared_task
def parse_monobank():
    from currency.models import Rate, Source
    url = 'https://api.monobank.ua/bank/currency'
    source, _ = Source.objects.get_or_create(
        code_name=MONOBANK_CODE_NAME,
        defaults={
            'source_url': url,
            'name': 'MonoBank'
        }
    )

    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()

    available_currency = {
        840: RateCurrencyChoices.USD,
        978: RateCurrencyChoices.EUR,
    }
    # UAH 980 Ukrainian hryvnia, USD 840 United States dollar, EUR	978	Euro

    for rate in rates:
        if rate['currencyCodeA'] not in available_currency:
            continue
        if rate['currencyCodeA'] in available_currency and rate['currencyCodeB'] in available_currency:
            continue

        buy = to_2_places_decimal(rate['rateBuy'])
        sale = to_2_places_decimal(rate['rateSell'])
        currency = rate['currencyCodeA']

        last_rate = Rate.objects.filter(
            currency=available_currency[currency],
            source=source
        ) \
            .order_by('-created') \
            .first()

        if hasattr(last_rate, 'pk'):
            if last_rate.buy != buy or last_rate.sale != sale:
                Rate.objects.create(
                    buy=buy,
                    sale=sale,
                    currency=available_currency[currency],
                    source=source,
                )
        else:
            Rate.objects.create(
                buy=buy,
                sale=sale,
                currency=available_currency[currency],
                source=source,
            )


@shared_task(autoretry_for=(ConnectionError,),
             retry_kwargs={'max_retries': 5})
def send_mail(subject, message):
    #  raise ConnectionError
    recipient = settings.DEFAULT_FROM_EMAIL
    from django.core.mail import send_mail
    # from time import sleep
    # sleep(10)
    send_mail(
        subject,
        message,
        recipient,
        [recipient],
        fail_silently=False,
    )


@shared_task
def parse_finance_ua():
    from currency.models import Rate, Source
    url = 'https://finance.ua/ru/currency'
    source, _ = Source.objects.get_or_create(
        code_name=FINANCE_UA_CODE_NAME,
        defaults={
            'source_url': url,
            'name': 'finance_ua'
        }
    )
    page = requests.get(url)
    if page.status_code != 200:
        raise ConnectionError

    soup = BeautifulSoup(page.text, "html.parser")
    all_rates = soup.findAll('table', class_='b-market-table_currency-cards table-layout-cards', limit=1)
    usd = []
    eur = []
    for data in all_rates:
        if data.find_all('td', class_='c1') is not None:
            d_c1 = data.find_all('td', class_='c1')
            usd.append(d_c1[0].text)
            eur.append(d_c1[1].text)
            if data.find_all('td', class_='c2') is not None:
                d_c2 = data.find_all('td', class_='c2')
                usd.append(d_c2[0].text[:5])
                eur.append(d_c2[1].text[:5])
                if data.find_all('td', class_='c3') is not None:
                    d_c3 = data.find_all('td', class_='c3')
                    usd.append(d_c3[0].text[:5])
                    eur.append(d_c3[1].text[:5])
    if len(usd) == 3:
        buy = to_2_places_decimal(usd[1])
        sale = to_2_places_decimal(usd[2])
        currency = RateCurrencyChoices.USD

        last_rate = Rate.objects.filter(
            currency=currency,
            source=source
        ) \
            .order_by('-created') \
            .first()

        if hasattr(last_rate, 'pk'):
            if last_rate.buy != buy or last_rate.sale != sale:
                Rate.objects.create(
                    buy=buy,
                    sale=sale,
                    currency=currency,
                    source=source,
                )
        else:
            Rate.objects.create(
                buy=buy,
                sale=sale,
                currency=currency,
                source=source,
            )

    if len(eur) == 3:
        buy = to_2_places_decimal(eur[1])
        sale = to_2_places_decimal(eur[2])
        currency = RateCurrencyChoices.EUR

        last_rate = Rate.objects.filter(
            currency=currency,
            source=source
        ) \
            .order_by('-created') \
            .first()

        if hasattr(last_rate, 'pk'):
            if last_rate.buy != buy or last_rate.sale != sale:
                Rate.objects.create(
                    buy=buy,
                    sale=sale,
                    currency=currency,
                    source=source,
                )
        else:
            Rate.objects.create(
                buy=buy,
                sale=sale,
                currency=currency,
                source=source,
            )
