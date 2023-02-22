from django.http import HttpResponse

from currency.models import Rate, ContactUs


def list_rates(request):
    qs = Rate.objects.all()
    result = []

    for rate in qs:
        result.append(f'id: {rate.id}, buy: {rate.buy}, sell: {rate.sell}, currency: {rate.currency}, '
                      f'source: {rate.source}, created: {rate.created} <br>')

    return HttpResponse(str(result))


def list_message(request):
    qs = ContactUs.objects.all()
    result = []

    for mes in qs:
        result.append(
            f'id: {mes.id}, email: {mes.email_from}, subject: {mes.subject}, message: {mes.message} <br>')

    return HttpResponse(str(result))
