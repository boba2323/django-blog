from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.urls import reverse_lazy
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse, reverse_lazy
from mptt.models import MPTTModel, TreeForeignKey
from django_ckeditor_5.fields import CKEditor5Field
# for the ratings
from django.db.models import Avg

# for images
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.validators import validate_image_file_extension

# to access STATIC_URL from settings.py
from django.conf import settings
# Create your models here.



class MyuserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("The Username field must be set")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email , password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True  # Ensure the user is a superuser
        user.save(using=self._db)
        return user
    
class Myuser(AbstractBaseUser, PermissionsMixin):
    # the permissionsmixin is needed to handle the error Myuser' object has no attribute 'get_all_permissions'
    # but apparently that didnt work
    # https://github.com/django/django/blob/5fcfe5361e5b8c9738b1ee4c1e9a6f293a7dda40/django/contrib/auth/models.py#L284
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = MyuserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        '''only the admin can return True for all permissions'''
        if self.is_active and self.is_admin:
        # Simplest possible answer: Yes, always
            return True
        return perm in self.get_all_permissions( obj=obj)

    def has_module_perms(self, blogapp):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Profile(models.Model):
    myuser = models.OneToOneField(Myuser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    small_status = models.CharField(max_length=150, blank=True)
    profile_desc = models.CharField(max_length=150, blank=True)
    # the defaut image isnt working so we use the get_image method. 
    # we need to point to the correct path in the bucket to get at the default image, or we could remove default and use the get_image method
    picture = models.ImageField(upload_to="profile-pictures/", 
                                # default="https://djangoblog-bucket.blr1.digitaloceanspaces.com/default/Default_pfp.jpg",
                                blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy("blogapp:index")
    
    # custom method for image and fallback image
    def get_image(self):
        if self.picture:
            return self.picture.url
        else:
            return settings.STATIC_URL + 'blogapp/images/Default_pfp.jpg'

# https://stackoverflow.com/questions/54976444/django-form-imagefield-validation-for-certain-width-and-height   
def validate_image(image):
    max_height = 650
    max_width = 1450
    min_height = 600
    min_width = 1400
    img = Image.open(image)
    height = img.height 
    width = img.width
    if width > max_width:
        raise ValidationError("Width is larger than what is allowed")
    if height > max_height:
        raise ValidationError("Height is larger than what is allowed")
    if width < min_width:
        raise ValidationError("Width is smaller than what is allowed")
    if height < min_height:
        raise ValidationError("Height is smaller than what is allowed")
  
#   validators=[validate_image],

class BlogPost(models.Model):
    title = models.CharField(max_length=50, unique=True)
    subtitle = models.CharField(max_length=100)
    date_written = models.DateTimeField(auto_now_add=True)
    body = CKEditor5Field('Body', config_name='extends')
    authors = models.ManyToManyField(Myuser)
    image = models.ImageField('Image', upload_to='blogpost-images/', validators=[validate_image, validate_image_file_extension], blank=True, null=True)

    def __str__(self):
        return f'object {self.title}'
    
    def get_absolute_url(self):
        print("getting absolute inside the authormodel")
        return reverse_lazy("blog:index")
    
    def average_rating(self) -> float:
        ratings_dict=Rating.objects.filter(post=self).aggregate(average_rating=Avg("rating"))
        ratings=ratings_dict['average_rating']
        return ratings or 0
    
    # custom method for image and fallback image
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return settings.STATIC_URL + 'blogapp/images/post/post-5.jpg'
    
class Rating(models.Model):
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.title}: {self.rating}"
    

class Comment(MPTTModel):
    text = models.TextField( )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=False)

    author_myuser = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['date_created']


