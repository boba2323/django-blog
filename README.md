# django-blog
A full blog made in django and other libraries such as celery, sendgrid. Packages with Docker. Uses compose.

## INSTRUCTIONS
the complete list of commands I had torunto get the thing running
1.	= docker volume create nginx_ssl
2.	= docker run --rm -v nginx_ssl:/mnt -v "/$(pwd):/host" busybox cp /host/example.com+5.pem /host/example.com+5-key.pem /mnt/
3.	If the volumes are running, we run with step 4 and skip 6.7
4.	= docker-compose -f docker_new_compose.dev.yml up --build
5.	= docker-compose exec django-web python manage.py migrate
6.	= docker-compose exec --user root django-web chown -R appuser:appuser /app/staticfiles
7.	=  docker-compose exec --user root django-web chown -R appuser:appuser /app/media
8.	= docker-compose exec django-web python manage.py collectstatic

to check if the folders in django has permissions
1.	= docker-compose exec django-web bash
2.	= ls


render has expired and a new database is needed. we pick neon. all DATABASE_RENDER  changed to DATABSE_ONLINE