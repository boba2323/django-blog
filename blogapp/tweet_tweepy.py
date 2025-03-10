import tweepy
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import JsonResponse

class TweetTweepy():
    def __init__(self, user, user_auth=False ):
        self.user = user

        # https://github.com/tweepy/tweepy/discussions/1974
        # If you're using a OAuth 2.0 Authorization Code Flow with PKCE access token, you can set the user_auth parameter to False, to use the access token to authenticate instead.
        self.user_auth=user_auth


        # look for the social account linked to the user
        try:
            self.social_account = SocialAccount.objects.get(user=user, provider="twitter_oauth2")
        # https://docs.djangoproject.com/en/5.1/ref/models/class/#django.db.models.Model.DoesNotExist
        except SocialAccount.DoesNotExist:
            raise ValueError("account not found")

        try:
            self.token = SocialToken.objects.get(account=self.social_account).token
            # good point to make a test
            print("heres the token retrived from the db", self.token)
            print('the type of the token is', type(self.token))
        except SocialToken.DoesNotExist:
            raise ValueError('social token does not exist')
        
        self.client = tweepy.Client(self.token)

    def make_tweet(self, message):
        try: 
            response=self.client.create_tweet(text=message, user_auth=False)
            return response
        except Exception as e:
            return JsonResponse({'error': e})
        


