# Django Blog
A blog titled Life of Mocha

#About The Project
A simple blog built with Django 4.2. It allows the owner of the blog to make posts and style them for the the viewers to see. Viewers can sign up and request the owner to be contributors to the blog as well. This app is designed to be production ready.

https://www.addwebsolution.com/blog/digitalocean-droplets-vs-app-platform 
Deployed on digital ocean app platform, a PaaS. Performs seamless code deployment direct from Git repositories such as GitHub

## Features
*	Ckeditor creates ability to insert images along with rich text content
*	2 groups, writers and travelers. Permissions are automatically created by a  migration and are managed in admin. Signals are used to create profiles of every user that joins. 
*	A search function to search for blog titles
*	Ability to sort posts by their author's names alphabetically
*	Can tweet author profiles/articles/etc. Uses X web intent to make tweets. It doesn’t require any API
*	Use of social apps to perform authentication
*	With mcert certificates, the django app can also be served on HTTPS
*   A well-made commenting and reply system that requires log in
*   A star rating system to review the posts. Also requries a log in.


## The tech that characterize the blog:
#### Backend and its other processes
*   Django 4.2 used as framework
*   Postgresql is used as a relational database to store our data
*	MPTT: Handles hierarchical data which means its great to build a nested comment section for the blog
*	Pagination keeps number of posts in the index page at 5 or at any desired number
*	Django-widget-tweaks for making customizable forms
*	Sendrid SMTP backend as email backend is used to handle emails
*	While sendgrid takes care of sending the email, the act of sending the email is queued so it doesn’t block the request response cycle
*	Celery and redis as a broker to take on the asynchronous task execution of sending emails for all auth outside the HTTP request-response cycle. This is helpful as sending email via SMTP or other third party packages can be slow. 
*	Redis is also used to maintain cache.

#### Frontend
*	Bootstrap. Great to work with for UI.
*   Django Template Language (DTL). Data is passed from the backend to templates via the context dictionary, enabling DTL to render dynamic content

#### DevOps and Deployment
*	App is dockerised. All the services exist in their own containers.
*   Gunicorn serves as the WSGI server in production
*   Nginx sits in front as reverse proxy for SSL termination and also to server media and static files
*	Whitenoise serves static files for the time being, basically lets gunicorn serve files

#### Storage and Caching
*   While all files are stored locally, this project is configured to connect with online Render database, Render redis and Digital Ocean Spaces to make it more production ready if desired. This way, storage and caching are handled by online servers.

#### Email
*   In production, SendGrid API will serve as emailbackend instead of SMTP.


## Explanation of some tech
Celery basically looks for tasks in blogapp/tasks.py and pushes a message to redis and celery pulls out it out and perform it. Look for it in celery.py in project module.

A send email function that takes in a emailmultipart object as argument is defined in the tasks.py and celery discovers it. The send_mail function in django all auth adapter is overridden to use the send email function from tasks.py. When triggered, the task is queued to redis and celery pulls it out to perform it.

We have two ways to make the app serve through https, by using certs and using the runserver plus command, or by using a nginx server and making it perform a reverse proxy

## How To Install

We would begin with acquiring some SSL certificates. I use MCERT certificates to for SSL. You can choose to use any other form of certficates. 

Heres how to obtain the mcert certs
Steps to Run Command Prompt with Elevated Privileges:
1.	Open an Elevated Command Prompt:
*	Click on the Start menu, type cmd or powershell.
*	Right-click on Command Prompt or PowerShell and select Run as administrator.
2.	Install mkcert:
*	Once the elevated Command Prompt or PowerShell window is open, run the following command:

```bash 
choco install mkcert
```
```sh
mkcert -install
```
```sh
mkcert example.com "*.example.com" example.test localhost 127.0.0.1 ::1
```
This will generate two files:
    1. example.com+5.pem
    2. example.com+5-key
https://github.com/FiloSottile/mkcert?tab=readme-ov-file 

### Note:
 To run the app with Django using the SSL instead of Nginx, we can run this command
```sh python manage.py runserver_plus --cert-file example.com+5.pem --key-file example.com+5-key.pem ```

To manage the database, it is advisable to install pgAdmin4

# Dockerizing The App
For best performance and ease, use WSL 2 to run docker. 
*	We use docker-compose.
*	Docker can be run as root in development, but is not recomended in production.
*	Docker must run in a linux environment or if on Windows, inside a WSL environment.
*	Containers are created for services, django-web, celery, redis, database, nginx. For production, nginx and database are not required. All services run inside docker.
*	We will run the application with gunicorn for production. It also supports multithreading among other benefits.
*   For serving our app over HTTPS, we need to use SSL certs. We have volume mounted the certs inside a volume we created in docker. Docker runs in a linux environment and store the certs in etc/nginx/ssl/.
*	In rare cases of issues, you can have both django and nginx handling HTTPS, which causes a redirect loop.


 The env file contains all the values required to make the right configurations for running the app in dev mode. It can also be set up for production like dev mode. To keep it at development mode, ENIVRONMENT_DEVELOPMENT=True
 For production, ENIVRONMENT_DEVELOPMENT=False

 ``` ini
# environment variables for mode
ENVIRONMENT_DEVELOPMENT=True
USE_SPACES=False

# django secret
SECRET_KEY=your-secret-key

# local postgresql database variables
DB_NAME=name-of-your-database
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db #we change to db  from localhost so it would match the database name in docker-compose
DB_PORT=5432

# Docker postgresql database variables
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_HOST=db
DATABASE=postgres

# Google secrets for django-allauth
GOOGLE_CLIENT_ID=your-secret
GOOGLE_CLIENT_SECRET=your-secret

TWITTER_API_KEY=your-secret
TWITTER_API_KEY_SECRET=your-secret

TWITTER_BEARER_TOKEN=your-secret
TWITTER_ACCESS_TOKEN=your-secret 
TWITTER_ACCESS_TOKEN_SECRET=your-secret

# Twitter OAuth2 secrets for django-allauth
TWITTER_0AUTH2_CLIENT_ID=your-secret
TWITTER_OAUTH2_CLIENT_SECRET=your-secret

# email variables
GMAIL_PASSWORD_SMTP=your-secret

# sendgrid
SENDGRID_API_KEY=your-secret
SENDGRID_FROM_EMAIL=your-email
DEFAULT_FROM_EMAIL=your-email

# Online database configuration
DATABASE_RENDER_PASSWORD=online-db-password
DATABASE_RENDER_NAME=online-db-name
DATABASE_RENDER_USER=online-db-secret
DATABASE_RENDER_HOST=online-db-secret
DATABASE_RENDER_PORT=5432
DATABASE_RENDER_URL=online-db-url

# Redis configuration. redis in render. we use rediss. emphasis on secure
REDISS_URL=online-rediss-url

# settings for DO SPACES for storage
AWS_ACCESS_KEY_ID=secret
AWS_SECRET_ACCESS_KEY=secret
AWS_STORAGE_BUCKET_NAME=secret
AWS_S3_ENDPOINT_URL=secret-url
DO_SPACES_CDN_END_POINT=secret-url 
```

## Run these commands to start your the app.
``` sh 
docker volume create nginx_ssl
```
```sh
docker run --rm -v nginx_ssl:/mnt -v "/$(pwd):/host" busybox cp /host/example.com+5.pem /host/example.com+5-key.pem /mnt/
```
```sh
docker-compose -f docker_new_compose.dev.yml up --build
```
```sh
docker-compose exec django-web python manage.py migrate
```
```sh
docker-compose exec --user root django-web chown -R appuser:appuser /app/staticfiles
```
```sh
docker-compose exec --user root django-web chown -R appuser:appuser /app/media
```
```sh
docker-compose exec django-web python manage.py collectstatic
```

Step 1. Creates a persistent volume in docker
Step2. Mounts the volume in the working directory in docker and copies the SSL certs. These certs will persist even after the containers are spun down
Step3. Spin up your containers with the specific development compose files
Step4. Migrate your models
Step5/6. Give permissions to your non root user to manage these subdirectories
Step7. Collects your static

To delete all docker containers
```sh docker rm $(docker ps -aq)```
To remove all your docker images
```sh docker rmi $(docker images -q)```
This is to remove your persistent volumes
```sh docker volume rm $(docker volume ls -q)```

If your volumes are still running, then you can begin with 4 and skip 6 and 7.
Set up your postgresql. Have pgadmin greatly aids managing your database
