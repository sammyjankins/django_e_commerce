import io

from celery import shared_task
from django.core.mail import EmailMessage

from myshop.settings import EMAIL_HOST_USER
from orders.models import Order
from orders.pdf import PDFReport


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop – Invoice no. {order.id}'
    message = f'Please, find attached the invoice for your recent purchase. '

    report = PDFReport()
    buffer = io.BytesIO(report.get_report(order))
    buffer.seek(0)
    value = buffer.getvalue()

    email = EmailMessage(subject,
                         message,
                         EMAIL_HOST_USER,
                         [order.email])
    email.attach(f'order_{order.id}.pdf',
                 value,
                 'application/pdf')
    email.send()
