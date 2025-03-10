import tweepy
import environ
import logging

logging.basicConfig(level=logging.DEBUG)

env = environ.Env()
environ.Env.read_env()

# CLIENT_ID=env('TWITTER_0AUTH2_CLIENT_ID')
REDICRECT_URI='https://127.0.0.1:8000/accounts/twitter_oauth2/login/callback/'
# we get this from our django all auth authorisation flow
auth_url='https://twitter.com/i/oauth2/authorize?client_id=N3RWQjdsdXk3Rlo5aENKaVJQT046MTpjaQ&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Ftwitter_oauth2%2Flogin%2Fcallback%2F&scope=tweet.write+tweet.read+users.read&response_type=code&state=dh42vhZXQb8hp5kE&access_type=online&code_challenge_method=S256&code_challenge=qP8DqpTyNowA2KXgDaGFciqZTm89midvs-bTkPdNXag'

# CLIENT_SECRET=env('TWITTER_OAUTH2_CLIENT_SECRET')
logger = logging.getLogger("tweepy")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="tweepy.log")
logger.addHandler(handler)

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id='N3RWQjdsdXk3Rlo5aENKaVJQT046MTpjaQ',
    redirect_uri=REDICRECT_URI,
    scope=[ "users.read",
            "tweet.read",
            'tweet.write',],
    # Client Secret is only necessary if using a confidential client
    client_secret='eYCuQ7amptBcF9h24fHBn0EfSBRsgssciPs6KYQczjJQXX83Zd',

)

# auth_url = oauth2_user_handler.get_authorization_url()
# print(oauth2_user_handler.get_authorization_url())

TWITTER_ACCESS_TOKEN='1877649991889494016-8siOiJk50sgvpwZBLYTviuA2NK7c51'

# access_token = oauth2_user_handler.fetch_token(auth_url)
client = tweepy.Client(TWITTER_ACCESS_TOKEN)
print(client)

