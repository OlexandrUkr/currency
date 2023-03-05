from django.urls import path

from currency.views import (
    RatesListView,
    RateCreateView,
    RateDetailView,
    RateUpdateView,
    RateDeleteView,
    MessagesListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MessageDetailView,
    SourcesListView,
    SourceCreateView,
    SourceUpdateView,
    SourceDeleteView,
    SourceDetailView
)

app_name = 'currency'


urlpatterns = [
    path('rate/list/', RatesListView.as_view(), name='rate-list'),
    path('rate/create/', RateCreateView.as_view(), name='rate-create'),
    path('rate/update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),
    path('rate/delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),
    path('rate/details/<int:pk>/', RateDetailView.as_view(), name='rate-details'),
    path('message/list/', MessagesListView.as_view(), name='message-list'),
    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),
    path('message/details/<int:pk>/', MessageDetailView.as_view(), name='message-details'),
    path('source/list/', SourcesListView.as_view(), name='source-list'),
    path('source/create/', SourceCreateView.as_view(), name='source-create'),
    path('source/update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),
    path('source/details/<int:pk>/', SourceDetailView.as_view(), name='source-details')
]
