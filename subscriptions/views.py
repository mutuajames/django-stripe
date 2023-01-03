import stripe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User

from .models import StripeCustomer


@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
def success(request):
    return render(request, 'success.html', {})

@login_required
def cancel(request):
    return render(request, 'cancel.html', {})

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
              client_reference_id = request.user.id if request.user.is_authenticated else None,
              success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
              cancel_url = domain_url + 'cancel/',
              payment_method_types = ['card'],
              mode = 'subscription',
              line_items = [
                {
                  'price': settings.STRIPE_PRICE_ID,
                  'quantity': 1,
                }
              ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
@csrf_exempt
def stripe_webhook(request):
  stripe.api_key = settings.STRIPE_SECRET_KEY
  endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
   
    # Fetch all required data from session
    client_reference_id = session.get('client_reference_id')
    stripe_customer_id = session.get('customer')
    stripe_subscription_id = session.get('subscription')

    #Get user and create new StripeConsumer
    user = User.objects.get(id=client_reference_id)
    StripeCustomer.objects.create(
      user = user,
      stripeCustomerId = stripe_customer_id,
      stripeSubscriptionId = stripe_subscription_id,
    )
    print(user.username + ' just subscribed.')
  return HttpResponse(status=200)