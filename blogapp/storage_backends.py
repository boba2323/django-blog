# https://testdriven.io/blog/django-digitalocean-spaces/#public-media-files

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# class StaticStorage(S3Boto3Storage):
#     location = 'static'
#     default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

    @property
    def querystring_auth(self):
        return False
    
class CkeditorStorage(S3Boto3Storage):
    """Custom storage for django_ckeditor_5 images."""
    location = 'ckeditor-images'
    default_acl = 'public-read'
    file_overwrite = False

    @property
    def querystring_auth(self):
        return False