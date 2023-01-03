from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='subscriptions-home'),
    path('config/', views.stripe_config, name='stripe-config'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
]