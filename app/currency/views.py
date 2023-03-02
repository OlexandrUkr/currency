from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from currency.models import Rate, ContactUs, Source
from currency.forms import SourceForm


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


def list_sources(request):
    sources = Source.objects.all()
    context = {
        'sources': sources
    }
    return render(request, 'list_sources.html', context)


def source_details(request, pk):
    source = get_object_or_404(Source, pk=pk)
    context = {
        'source': source
    }
    return render(request, 'source_details.html', context)


def source_create(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        form = SourceForm()

    context = {
        'form': form
    }
    return render(request, 'source_create.html', context)


def source_update(request, pk):
    source = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        form = SourceForm(instance=source)

    context = {
        'form': form
    }
    return render(request, 'source_update.html', context)


def source_delete(request, pk):
    source = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        context = {
            'source': source
        }
        return render(request, 'source_delete.html', context)
