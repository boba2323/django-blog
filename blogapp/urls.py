from django.urls import path

from . import views

app_name="blogapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index" ),
    # path('accounts/signup/', views.SignUpView.as_view(), name="sign-up" ),
    path('users/', views.UserView.as_view(), name="users" ),
    path('users/profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),
    path("profile-view/<int:user_pk>/update/<int:pk>", views.ProfileUpdateForm.as_view(), name="profile-update"),
    path('create-post/', views.PostCreateView.as_view(), name="create-post"),
    path("post/<int:pk>/", views.PostCommentDetailView.as_view(), name="post-detail"),
    path('users/profile/<int:user_pk>/<int:pk>', views.BlogPostDeleteView.as_view(), name="post-delete"),
    path('users/profile/blog-update/<int:pk>', views.BlogPostUpdateFormView.as_view(), name="post-update"),
    path('email/', views.EmailView.as_view(), name="email"),
    # checks what protocols are being used
    path('protocol/', views.check_protocol, name='protocols')
    ]