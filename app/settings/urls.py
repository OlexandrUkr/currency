from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.urls import views

from currency.views import ProfileView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account/', include('account.urls')),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change.html'),
    path('password_change/done/', views.PasswordChangeView.as_view(), name='password_change_done.html'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('__debug__/', include('debug_toolbar.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('currency/', include('currency.urls'))
]
