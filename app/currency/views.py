from django.http import HttpResponse
from django.shortcuts import render

from currency.models import Rate, ContactUs


def list_rates(request):
    rates = Rate.objects.all()
    context = {
        'rates': rates
    }
    return render(request, 'list_rates.html', context)


def list_message(request):
    messages = ContactUs.objects.all()
    context = {
        'messages': messages
    }
    return render(request, 'list_message.html', context)
