import django_filters

from currency.models import Rate, Source, ContactUs


class RateFilter(django_filters.FilterSet):

    class Meta:
        model = Rate
        fields = ['buy', 'sale', 'source']


class SourceFilter(django_filters.FilterSet):

    class Meta:
        model = Source
        fields = ['id', 'name', 'code_name']


class ContactUsFilter(django_filters.FilterSet):

    class Meta:
        model = ContactUs
        fields = ['name', 'email_from', 'subject']
