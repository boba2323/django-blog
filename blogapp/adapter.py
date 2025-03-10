# https://github.com/pennersr/django-allauth/blob/main/allauth/socialaccount/adapter.py
# most of the edits are redundant and make no impact other than sendmail


from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# addming the imports below because im over-writing a method
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import (
    valid_email_or_none,
)
from allauth.account.adapter import get_adapter as get_account_adapter

# adding the import for my custom model
from django.contrib.auth import get_user_model

# for debugging
import logging
logger = logging.getLogger(__name__)

# for celery
from .tasks import send_mail_celery_func

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        user= super().new_user(request, sociallogin)
        print('new user being created')
        print('user', user)
        print(sociallogin)
        print('request', request)
        if user.password:
            print("in new user, password", user.password)
        if user.has_usable_password():
            print("in new user.... user has usable password")
            print("in new user, password", user.password)
            # user.set_unusable_password=lambda:None
            # user.save()
        else:
            print("in new user....no usable passwords")
        return user

    def populate_user(self, request, sociallogin, data):
        # user = super().populate_user(request, sociallogin, data)
        # i commented out the line above and added whats below me
        print('POPULATE USER')
        print(data)
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        name = data.get("name")
        user = sociallogin.user
        # user.set_unusable_password()
        # print('deliberate passsword unset', user.password)
        user_username(user, username or "")
        user_email(user, valid_email_or_none(email) or "")
        name_parts = (name or "").partition(" ")
        user_field(user, "first_name", first_name or name_parts[0])
        user_field(user, "last_name", last_name or name_parts[2])
        if user.password:
            print("populate, user password ",user.password)
        print('populating data...')
        if user.has_usable_password():
            print("populating fields....has usable password")
        else:
            print("populating fields....no usable passwords")  
        return user

    def save_user(self, request, sociallogin, form=None):
        print('save method being called?')
        # user = super().save_user(request, sociallogin, form)
        # print("we inside the custom adapter save method")
        # print(user)
        # if user.password:
        #     print("save_user, user password ",user.password)
        # print(user.email)
        # if user.has_usable_password():
        #     print("newly created user has usable password")
        #     # user.set_unusable_password=lambda:None
        #     # user.save()
        # else:
        #     print("no usuable password in save user")
        # return user
    
        # we comment out everything above to overwrite this method
        Customuser= get_user_model()
        u = sociallogin.user
        print(u)
        try:
            current_user=Customuser.objects.get(email=u.email)
            print('current user found with the same email in local account', current_user)
            if current_user:
                get_account_adapter().populate_username(request, u)
        except:
            print('no current user not found')
            u.set_unusable_password()
            get_account_adapter().populate_username(request, u)
            
        # u.set_unusable_password() comment this out since we dont want to unset password
        # if form:
            # no form is available as we are only doing a case of AUTOSIGNUP,
            # hence the statement below is not needed
            # get_account_adapter().save_user(request, u, form)
        # else:
        sociallogin.save(request)
        return u
        
    
    def pre_social_login(self, request, sociallogin):
        # for debugging
        logger.info(f"Social login data: {sociallogin.account.extra_data}")
        print('in pre social login')
        Customuser= get_user_model()
        u = sociallogin.user
        try:
            current_user=Customuser.objects.get(email=u.email)
            print('current user found with the same email in local account', current_user)
            if current_user:
                get_account_adapter().populate_username(request, u)
        except:
            print('no current user not found')
            u.set_unusable_password()
            get_account_adapter().populate_username(request, u)



    def send_mail(self, template_prefix: str, email: str, context: dict) -> None:
        # msg is standard from https://github.com/pennersr/django-allauth/blob/main/allauth/account/adapter.py#L154
        # render_mail is a method from django all auth. it basically returns a EmailMultiAlternatives object
        msg= super().render_mail(template_prefix, email, context)
        send_mail_celery_func.delay(msg)