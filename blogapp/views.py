# run this command to start
# python manage.py runserver_plus --cert-file example.com+5.pem --key-file example.com+5-key.pem

from django.shortcuts import render
from django.db.models import Min
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import Http404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.db.models import F
from django.views import generic
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.views.generic import FormView
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import localtime
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate
# Create your views here.
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse
from .form import CustomUserForm, ProfileForm, CommentForm, BlogPostForm
from .models import Profile, BlogPost, Comment, Rating
# for email
from django.core.mail import send_mail

import tweepy
import environ, os

# import the custom twitter class
from blogapp.tweet_tweepy import TweetTweepy

# env = environ.Env()
# consumer_key= "your_secret_key"
# consumer_secret = "your-api-secret-key"
# access_token = "your-access_token"
# access_token_secret ="your-access_token_secret"
# auth = tweepy.OAuth1UserHandler(
#     env('API_KEY'), env('API_KEY_SECRET'), env('ACCESS_TOKEN'), env('ACCESS_TOKEN_SECRET')
# )
# api = tweepy.API(auth)


User = get_user_model()

class IndexView(generic.ListView):
    template_name="blogapp/index.html"
    context_object_name="posts"
    model = BlogPost
    paginate_by = 6

    login_url = '/accounts/login/'


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # for post in queryset:
        #     post.short_content = post.body[:250] + "..." if len(post.body) > 280 else post.body
        query = self.request.GET.get('s')
        by_author = self.request.GET.get('a')
        if query:
            return queryset.filter(title__icontains=query)
        if by_author:
            
            q_set = queryset.annotate(author_name=Min('authors__username'))
            return q_set.order_by('author_name')
        else:
            return queryset.order_by('-date_written') 
        

        
# API for rating

    def post(self, request):
        if not request.user.is_authenticated:
            # If the user is not authenticated, return a forbidden response or redirect them
            return redirect(reverse_lazy('login'))
        else:
            rating =request.POST.get('rating-value-key')
            # print(request.POST.get)
            post_id = request.POST.get('input-field')
            # print('post')
            # print((rating))
            user=request.user
            # print(user)
            # print(post_id)
            blog=BlogPost.objects.get(id=post_id)
            rating_lqueryset = Rating.objects.all()
            if rating_lqueryset:
                try:
                    existing_rating=Rating.objects.get(user=user, post=blog)
                    existing_rating.delete()
                except Exception as e:
                    # print(e)
                    print("no such rating for user and post")
            rating= Rating.objects.create(user=user, post=blog, rating=rating)
        return redirect(reverse_lazy("blogapp:index"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # stars, making sure the user ratings are dispplayed besides the average ratings

        # cuurent_user_rating = Rating.objects.filter(user=self.request.user, post=post)
        # if cuurent_user_rating:
        #     context["your_ratings"]=cuurent_user_rating[0].rating
        #     print("the ocntext of ratings" ,context["your_ratings"])
        # else:
        #     context['your_ratings']= 4
        return context
        



# class SignUpView( generic.CreateView):
#     form_class = CustomUserForm
#     success_url = reverse_lazy("blogapp:index")
#     template_name = "blogapp/signup.html"
#     # def get(self, request, *args, **kwargs):
#     #     # Create a new, empty form instance for GET requests
#     #     form = self.get_form()
#     #     return self.render_to_response(self.get_context_data(form=form))

#     def form_invalid(self, form):
#         # Render the form with errors for POST requests
#         return super().form_invalid(form)
    
#     def form_valid(self, form):
#         # Handle valid form data here
#         # Example: authenticate user or save data
#         return super().form_valid(form)
    
class ProfileView(generic.DetailView):
    template_name = "blogapp/profile.html"
    model = Profile

    def get_object(self, queryset = None):
        try:
            return super().get_object(queryset)
        except Http404:
            return redirect(reverse_lazy("blogapp:index"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['logged_user'] = self.request.user
        context['author_id'] = profile_user.myuser.id
        context['logged_user_id'] = self.request.user.id
        print('author_id=', profile_user.myuser.id, "logged_id=", self.request.user.id   )
        return context
    
    # post user to social media
    # tweepy isnt really required for the user to make a status on post apparently. the web based method is sufficient
    # we can use tweepy to authomate tweets later if we feel like it

    # https://developer.x.com/en/docs/x-for-websites/tweet-button/guides/web-intent
    def post(self, request, *args, **kwargs):
        user=request.user
        print("inside the profile, check user", user)
        from urllib.parse import urlencode
        query=urlencode({
            'text':"Something about our writer1",
            'url':request.build_absolute_uri(),   
        })

        twitter_url=f"https://twitter.com/intent/tweet?{query}"
        return HttpResponseRedirect(twitter_url)
        # if user:
        #     # tweet_provider =TweetTweepy(user)
        #     # # request.get_full_path() since we need the query params
        #     # tweet_provider.make_tweet("request.get_full_path(dsds) w2")
        #     # print("are we posting?")
        #     # return JsonResponse({'message':"tweeted"})
        #     # a prefilled status ?
        #     return HttpResponseRedirect("https://twitter.com/intent/tweet")
        # return JsonResponse({'error':'no auth'})
        
        

    
class UserView(generic.ListView):
    template_name="blogapp/users.html"
    model = User
    context_object_name="users"
    
    def get_queryset(self):
        query = User.objects.filter(groups__name="Writer")
        return query

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_in'] = "youre logged in"
        else:
            context['user_in'] = "youre logged out"
        context['extra'] =' more data'
        return context
    

class ProfileUpdateForm(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin,  generic.UpdateView):
    # permissions

    permission_required=['blogapp.change_profile', 'blogapp.add_profile']
    model = Profile 
    # form_class = ProfileForm
    template_name = "blogapp/profileform.html"
    fields = [ "first_name", "last_name","small_status", "profile_desc", "picture"]
    # one to one field is not displayed here or in the modelform in form.py
    login_url = reverse_lazy("blogapp:users")
    success_url = reverse_lazy("blogapp:users")

    def test_func(self):  
        '''the test func is executed before the form is processed'''
        profile_object = self.get_object()
        # print(type(self.request.user))
        user_id = self.request.user.id
        profile_form_id = profile_object.myuser.id
        # print(user_id, profile_form_id )
        return user_id == profile_form_id
    
    def form_valid(self, form):
        # print(type(self.request.user))
        print("Form is valid:", form.cleaned_data)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        form = self.get_form()
        context =  super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        context['form_id'] = form.instance.myuser.id
        return context
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Change the label of a field dynamically
        form.fields["small_status"].label = "Status"
        form.fields["profile_desc"].label = "About you"
        return form
    

    
class PostCreateView(PermissionRequiredMixin, generic.CreateView):
    # permissions
    
    permission_required='blogapp.add_blogpost'
    model = BlogPost
    fields = ["title", "subtitle", "body", 'image'] 
    template_name="blogapp/blogcreate.html"
    success_url = reverse_lazy('blogapp:index')
    
    def form_valid(self, form):
        post_instance = form.save()
        post_instance.authors.add(self.request.user)
        # print(object)
        post_instance.save()
        # form.instance.created_by = self.request.user
        return super().form_valid(form)
    

class PostDetailView(generic.DetailView):
    model = BlogPost
    template_name = "blogapp/detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_id = self.object.id
        # add the current viewing id to the session
        recently_viewed = request.session.get('recently_viewed', [])
        if post_id not in recently_viewed:
            recently_viewed.insert(0, post_id)
            if len(recently_viewed) > 3:  # Limit to 5 posts
                recently_viewed.pop()
        
        request.session['recently_viewed'] = recently_viewed
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        print("comment context")
        # stars, making sure the user ratings are dispplayed besides the average ratings
        if self.request.user.is_authenticated:
            cuurent_user_rating = Rating.objects.filter(user=self.request.user, post=post)
            if cuurent_user_rating:
                context["your_ratings"]=cuurent_user_rating[0].rating
                # print("the ocntext of ratings" ,context["your_ratings"])
            else:
                context['your_ratings']= 0

        context['form'] = CommentForm()
        context["comments"] = self.object.comment_set.all()
        recently_viewed_ids = self.request.session.get('recently_viewed', [])
        recently_viewed_posts = BlogPost.objects.filter(id__in=recently_viewed_ids)
        recently_viewed_posts = sorted(recently_viewed_posts, key=lambda post:recently_viewed_ids.index(post.id))
        context['recently_viewed_posts'] = recently_viewed_posts
        # print("fucl", cuurent_user_rating[0].rating)
        # print(type(cuurent_user_rating[0].rating))
        return context
    
class PostCommentFormView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, FormView):
    # permissions

    permission_required=['blogapp.add_comment', 'blogapp.change_comment', 'blogapp.view_comment']
    template_name = 'blogapp/detail.html'
    form_class = CommentForm
    model = BlogPost
    
    def post(self, request, *args, **kwargs):
        post_data=request.POST
        print('this is the post data' ,post_data)
        # checking the request.POST and look to see data from each form
# star review system in the post detail but we have two forms here actually
        rating =request.POST.get('rating-value-key')
        post_id = request.POST.get('input-field')
        user=request.user
        # blog=BlogPost.objects.get(id=post_id)
        rating_lqueryset = Rating.objects.all()
        # print(rating_lqueryset)
        # if rating_lqueryset:
        #     try:
        #         existing_rating=Rating.objects.get(user=user, post=blog)
        #         existing_rating.delete()
        #     except Exception as e:
        #         print(e)
        #         print("no such rating for user and post")
        # rating= Rating.objects.create(user=user, post=blog, rating=rating)

        print("works for post?")
        self.object = self.get_object()
        if "comment" in request.POST or "reply" in request.POST:
# notes: maybe the reqeust.POST contains a lot of extra information. passing it to the commentform instance is a bit of a
# move since all that extra data is not necessary and to clean it, some extra work in form validation? handling is done
# we could do a better job of handling the data before passing it into the instance. teh resquest.POST contains things like
# csrf token, the rating value, the input field, the comment text, the reply text, the reply button, the comment button and other irrelevant data 

            form_instance = CommentForm(request.POST)
            if not form_instance.is_valid():
                print(form_instance.errors)
                # print("fucked")
            if form_instance.is_valid():
                try:
                    parent = form_instance.cleaned_data['parent']  #reply to comment
                except:
                    parent=None       #top-level comment
                form_instance.instance.parent = parent
                form_instance.instance.author_myuser = self.request.user
                form_instance.instance.parent_post = self.get_object()
                form_instance.save()
                return super().post(request, *args, **kwargs)
            
        elif "rating-value-key" in request.POST:
            post_data=request.POST
            print('this is the ratiing data' ,post_data)
            # checking the request.POST and look to see data from each form
    # star review system in the post detail but we have two forms here actually
            rating =request.POST.get('rating-value-key')
            post_id = request.POST.get('input-field')
            user=request.user
            blog=BlogPost.objects.get(id=post_id)

            rating_lqueryset = Rating.objects.all()
            # print(rating_lqueryset)
            try:
                existing_rating=Rating.objects.get(user=user, post=blog)
                existing_rating.delete()
            except Exception as e:
                print(e)
                print("no such rating for user and post")
            rating= Rating.objects.create(user=user, post=blog, rating=rating)

            print("works for post?")

        # this is for tweeting
        elif "tweet" in request.POST:
            pass

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blogapp:post-detail', kwargs={'pk': self.object.id})


class PostCommentDetailView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)
    


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin,  generic.DeleteView):
    # permissions

    permission_required='blogapp.delete_blogpost'
    model = BlogPost
    template_name="blogapp/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blogapp:profile")

    def test_func(self):  
        '''the test func is executed before the form is processed'''
        blog_object = self.get_object()
        # print(type(self.request.user))
        user_id = self.request.user.id
        post_author = blog_object.authors.all()[0]
        author_id=post_author.id
        # print(user_id, author_id )
        return user_id == author_id
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile_id"] = self.request.user.id
        return context
    
    # needs overide the get_success_url since we need a id for returning to the user profile
    def get_success_url(self):
        return reverse_lazy('blogapp:profile', kwargs={'pk': self.request.user.id })
    
class BlogPostUpdateFormView(LoginRequiredMixin, PermissionRequiredMixin,  UserPassesTestMixin,  generic.UpdateView):
    # permissions

    permission_required=['blogapp.change_blogpost', 'blogapp.add_blogpost']
    model = BlogPost
    # adding the form that we want the update view to use
    form_class = BlogPostForm
    # fields = ["title", "subtitle", "body", 'image']
    template_name="blogapp/blogcreate.html"
    login_url = reverse_lazy("blogapp:users")
    # success_url = reverse_lazy("blogapp:users") success url no longer needed

    def test_func(self):  
        '''the test func is executed before the form is processed'''
        blog_object = self.get_object()
        user_id = self.request.user.id
        post_author = blog_object.authors.all()[0]
        author_id = post_author.id
        user_id = self.request.user.id
        return user_id == author_id

    # delete the form_valid method

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('blogapp:post-detail', kwargs={'pk': self.object.id })
    
    
class EmailView(generic.TemplateView):
    template_name='email/test.html'

    def post(self, request, *args, **kwargs):
        
        try:
            send_mail(
                "Subject here",
                "Here is the message.",
                "rajkumarmech95@gmail.com",
                ["deadryefield@gmail.com"],
                fail_silently=False,
            )
        except:
            return HttpResponse("EMAIL FAILED TO SEND")
        
        return redirect(reverse_lazy("blogapp:index"))

# checking which protocol we are using
def check_protocol(request):
    return JsonResponse({"protocol": request.scheme})