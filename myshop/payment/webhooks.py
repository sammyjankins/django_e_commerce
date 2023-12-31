import os

import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stripe.error import SignatureVerificationError

from orders.models import Order
from shop.recommender import Recommender
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.environ.get('STRIPE_WEBHOOK_SECRET'))
    except ValueError:
        return HttpResponse(status=400)
    except SignatureVerificationError:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)
            r = Recommender()
            r.products_bought([item.product.id for item in order.items.all()])

    return HttpResponse(status=200)
