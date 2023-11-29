# django_e_commerce
Implementation of an online store based on Antonio Mele's book 'Django 4 by Example' containerized using Docker Compose.

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
