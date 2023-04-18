from rest_framework.routers import DefaultRouter

from currency.api.views import RateViewSet, SourceViewSet, ContactUsViewSet

# from currency.api.views import RateApiView, RateDetailApiView

app_name = 'api-currency'

router = DefaultRouter()
router.register(r'rates', RateViewSet, basename='rates')
router.register(r'sources', SourceViewSet, basename='sources')
router.register(r'contact-us', ContactUsViewSet, basename='contact-us')

urlpatterns = [
    # path('rates/', RateApiView.as_view(), name='rates-list'),
    # path('rates/<int:pk>/', RateDetailApiView.as_view(), name='rates-details')
]

urlpatterns += router.urls
