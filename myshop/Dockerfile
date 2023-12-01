FROM python:3.10-alpine

RUN mkdir code
WORKDIR code

RUN apk update && apk upgrade && apk --no-cache add curl
RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD . /code/

CMD python ./utils/check_db_connection.py \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; from django.core import management; User = get_user_model(); User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists() or management.call_command('createsuperuser', interactive=False)" \
    && python manage.py collectstatic --no-input \
    && gunicorn myshop.wsgi:application --bind 0.0.0.0:8000
