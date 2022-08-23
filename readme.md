# Django template in docker with docker-compose

### Features of the template:

#### Project features:
* Docker/Docker-compose environment
* Added JWT user authenticating system (register, verify email, login, logout)
* Celery worker
* Redis service as message broker for queue
* Swagger in Django Admin Panel
* Redefined default User model (auth_app.models.py)
* MailHog integration

### How to use:

#### Clone the repo:

    git clone https://github.com/Olim2508/django-docker-template.git

#### Run the local develop server:

    docker-compose up -d --build
    docker-compose logs -f
    
##### Server will bind 8010 port. You can get access to server by browser [http://localhost:8010](http://localhost:8010)


##### For testing mail backend you can use MailHog service
    docker-compose -f docker-compose.yml -f docker/modules/mailhog.yml up -d --build

##### To create superuser run the command:
    docker-compose exec web python manage.py createsuperuser


<b>Don't forget to set SMTP mail backend in settings</b>




