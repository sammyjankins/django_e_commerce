# django_e_commerce
Implementation of an online store based on Antonio Mele's book 'Django 4 by Example' containerized using Docker Compose.

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/1ef2866b-47a2-4dca-8823-ee27ad69cdce)

# Instructions for building and launching the service

## Dependencies

Make sure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Project

1. Clone the repository:
```
git clone https://github.com/sammyjankins/django_e_commerce.git
```
2. Go to the project directory:

```
cd django_e_commerce/myshop
```
3. Fill the .env.project and .env.postgres files with actual data following .env.project.template and .env.postgres.template.

4. Build and start the containers:

```
docker-compose up -d
```

Migrations will be applied and superuser will be created automatically. Superuser credentials will be taken from the .env.project file.

5. Check that the containers are running:

```
docker ps
```

## Using the Project

Open the application in your browser:

```
http://localhost:80/
```

Log in to the admin panel using the credentials created in step 5:

```
http://localhost:80/admin/
```

# Features

## Coupon System

Using the admin panel you can create and manage discount coupons. Discount information will be stored in the order data.

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/a9d00b42-541f-41ac-837e-14725657dd4c)

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/77b7e0b3-d18d-400e-9467-252629ff66da)

## Email notifications

The application sends email notifications that indicate the creation of an order and payment notifications that contain an invoice in PDF format. This functionality is implemented using Сelery and RabbitMQ.

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/921a3a2c-e545-45c4-bb38-ab6cb87635af)

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/c41d7ca6-5385-4416-960a-6837f5d1ed95)

## Recommendations

The application has a recommendation system. This functionality is implemented using Redis.

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/a79b944b-7a94-4978-ae66-120719a37a5f)

## Stripe

The application uses Stripe as a payment system.

![image](https://github.com/sammyjankins/django_e_commerce/assets/26933434/8f466605-7467-4769-be05-a7dfc7a67926)
