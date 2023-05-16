from django_filters import rest_framework as filters
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import filters as rest_framework_filters

from currency import constants
from currency.filters import RateFilter, ContactUsFilter
from currency.api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from currency.choices import RateCurrencyChoices
from currency.models import Rate, Source, ContactUs
from currency.paginators import RatesPagination, ContactUsPagination
from currency.throttlers import AnonCurrencyThrottle


# class RateApiView(generics.ListCreateAPIView):
#     queryset = Rate.objects.all().select_related('source')
#     serializer_class = RateSerializer  # json.dumps, json.loads
#
#
# class RateDetailApiView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rate.objects.all()
#     serializer_class = RateSerializer

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatesPagination
    permission_classes = (AllowAny,)
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = RateFilter
    ordering_fields = ('id', 'created', 'buy', 'sale')
    throttle_classes = (AnonCurrencyThrottle,)

    @action(detail=False, methods=('GET',))
    def latest(self, request, *args, **kwargs):
        latest_rates = []

        cached_rates = cache.get(constants.LATEST_RATE_CACHE)
        if cached_rates:
            return Response(cached_rates)

        for source_obj in Source.objects.all():
            for currency in RateCurrencyChoices:
                latest = Rate.objects.filter(
                    source=source_obj,
                    currency=currency) \
                    .order_by('-created') \
                    .first()

                if latest:
                    latest_rates.append(RateSerializer(instance=latest).data)

        cache.set(constants.LATEST_RATE_CACHE, latest_rates, 60 * 60 * 24 * 7)

        return Response(latest_rates)


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (AllowAny,)


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = ContactUsPagination
    permission_classes = (AllowAny,)
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    filterset_class = ContactUsFilter
    ordering_fields = ('id', 'created', 'name', 'email_from', 'subject')
    search_fields = ['name', 'email_from']
