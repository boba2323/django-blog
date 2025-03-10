from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Profile, Comment, BlogPost
from allauth.account.forms import SignupForm

# dealing with customising the clear image input we see when an image already exists
from django.forms.widgets import ClearableFileInput 
from django.utils.safestring import mark_safe

User = get_user_model()

class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})
    


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [ "first_name", "last_name","small_status", "profile_desc", "picture"]
        # labels={
        #     'small_status':"Status",
        #     "profile_desc": "About you"
        # }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']

class MyCustomSignupForm(SignupForm):

    # fields customized dynamically to use placeholders. 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':' Custom form Username'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})
    
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

class CustomImageorFileClearingWidget(ClearableFileInput):
    # https://github.com/django/django/blob/stable/5.1.x/django/forms/widgets.py#L460
    # taken from github source
    clear_checkbox_label = mark_safe("Yes")
    initial_text = mark_safe("<span class='fst-italic'>This is the current image</span>")
    input_text = ""
    template_name = "widgets/customclearablefile.html"
    checked = False


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'subtitle', 'body',  'image']
        # adding the custom widget to the image attribute and assiging the id
        # that we have previeoulsy assigned to this field
        widgets = {
            "image": CustomImageorFileClearingWidget(attrs={"id":'custom-image-upload'}),
        }