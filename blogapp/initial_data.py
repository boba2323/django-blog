from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission

def populate_groups(apps, schema_editor):
	
# """This function is run in migrations/0002_initial_data.py as an initial
# data migration at project initialization. it sets up some basic model-level
# permissions for different groups when the project is initialised.
# https://dandavies99.github.io/posts/2021/11/django-permissions/#goal-2-set-up-groups-when-the-project-is-initialised-using-a-data-migration
# Maintainer: Full permissions over the batteryDB app to add, change, delete, view
# data in the database, but not users.
# Read only: Not given any initial permissions. View permission is handled on a
# per instance basis by Django Guardian (more on that later!).
# """

# Create user groups

    roles =["Writer", "Traveller"]

    for name in roles:
        Group.objects.get_or_create(name=name)


    # when we run second or third migrate using create() causes error psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "auth_group_name_key"
# DETAIL:  Key (name)=(Writer) already exists.
# hence we replace create with get_or_create


    # Permissions have to be created before applying them
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    # Assign model-level permissions to maintainers 
    # all_perms = Permission.objects.all()
    # all model permissions
    model_permissions = Permission.objects.filter(content_type__app_label__exact="blogapp")

    Group.objects.get(name="Writer").permissions.add(*model_permissions)

    # comment add, view and change permissions for traveller
    all_view_permissions = model_permissions.filter(codename__icontains="view")
    comment_permissions = model_permissions.filter(codename__icontains='comment')
    comment_ex_del_permissions=comment_permissions.exclude(codename__icontains='delete')

    # all auth permissions
    account_permissions = model_permissions.filter(codename__icontains='account')
    socialaccount_permissions = model_permissions.filter(codename__icontains='socialaccount')
    # travller_permissions = all_view_permissions.union(comment_ex_del_permissions)

    travller_permissions = (
    all_view_permissions 
    | comment_permissions 
    | comment_ex_del_permissions 
    | account_permissions 
    | socialaccount_permissions
)

    Group.objects.get(name="Traveller").permissions.add(*travller_permissions)

# <QuerySet [<Permission: blogapp | myuser | Can view myuser>, <Permission: blogapp | profile | Can view profile>, <Permission: blogapp | blog post | Can view blog post>, <Permission: blogapp | comment | Can add comment>, <Permission: blogapp | comment | Can change comment>, <Permission: blogapp | comment | Can view comment>]>

	
	
	

    # Writer_perms = [i for i in all_perms if i.content_type.app_label == "blogapp"]
    # Group.objects.get(name="Writer").permissions.add(*Writer_perms)
    #The *permissions syntax unpacks the list of permissions and passes them as individual arguments

    # python manage.py makemigrations --empty blogapp run this for new migration file