from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import Group

# signals for twitter oauth2 email requirement
from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect
from django.http import HttpResponse
from allauth.exceptions import ImmediateHttpResponse

Myuser = get_user_model()

@receiver(post_migrate)
def create_traveller_group(sender, **kwargs):
    Group.objects.get_or_create(name="Traveller")
    Group.objects.get_or_create(name="Writer")


@receiver(post_save, sender=Myuser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only create a Profile for newly created Users
        Profile.objects.create(myuser=instance)
        # for groups
        traveller, is_created = Group.objects.get_or_create(name="Traveller")
        # get_or_create returns a tuple (group, boolean)
        if not instance.is_admin and instance.id != 1:
            # the admin is not added to traveller
            instance.groups.add(traveller)
            instance.save()

# signal to add the email for oauth2
@receiver(pre_social_login)
def pre_social_login_callback(sender, request, sociallogin, **kwargs):
    user = sociallogin.user

    # If email is missing, redirect to the email entry form
    # or add a feature to let them access email manager
    if not user.email:
        print(user.username)
        print("no email present") #first test with print statements
        # raise ImmediateHttpResponse(HttpResponse("Login failed: Email is required.", status=400))
        # return redirect('add_email')  # Redirect to a page where they can enter their email


        # signal comes from apps/py myuser

