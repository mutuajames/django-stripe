from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='subscriptions-home'),
    path('config/', views.stripe_config, name='stripe-config'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
]