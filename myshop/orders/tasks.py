from celery import shared_task
from django.core.mail import send_mail

from myshop.settings import EMAIL_HOST_USER
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task for sending email notification upon successful order creation.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (f'Dear {order.first_name},\n\n'
               f'You have successfully placed an order.'
               f'Your order ID is {order.id}.')
    mail_sent = send_mail(subject, message,
                          EMAIL_HOST_USER,
                          [order.email])
    return mail_sent
