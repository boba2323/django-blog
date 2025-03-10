

# Use the official Python runtime image
FROM python:3.12.6 
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# for creating the directory where the certs will eixst
RUN mkdir -p /etc/nginx/ssl
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# system dependencies
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc


# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/
 
# Expose the Django port
EXPOSE 8000
 


# Run Django’s development server
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000" , "--cert-file", "/app/example.com+5.pem", "--key-file", "/app/example.com+5-key.pem"]
