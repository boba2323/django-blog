from django.apps import AppConfig


class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogapp'

    def ready(self):
        import blogapp.signals  # Ensure signals are loaded when the app starts
        # signal to recevier to create a profile object the moment a user is created
