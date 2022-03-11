# from response.EngagementResponse import EngagementResponse
from . import credentials
from .EngagementResponse import EngagementResponse
#PRIMER PASO
#pip install tweepy (hacerlo directamente en el consola)

import tweepy
import warnings
warnings.filterwarnings('ignore')

#pip install textblob (hacerlo directamente en el consola)
#pip install matplotlib (hacerlo directamente en el consola)

auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
api = tweepy.API(auth)


################################ PARA BUSCAR POR USUARIO ##################################################################
def getEngagement(user):
    auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    api = tweepy.API(auth)

    # Contadores
    num_likes = 0
    num_retweet = 0
    num_coment = 0

    # Calcular numero de seguidores para ese usuario
    _user = api.get_user(screen_name=user)
    followers_count = _user.followers_count

    # Engagement
    tweets = api.user_timeline(screen_name=user, count = 200)
    for tweet in tweets:
        num_likes=num_likes+tweet.favorite_count
        num_retweet=num_retweet+tweet.retweet_count
        num_coment= num_coment+len(tweet.entities['hashtags'])

    total=(num_likes + num_retweet + num_coment) / followers_count
    print("ENGAGEMENT ACTUAL PARA ",user,"ES: ", total)
    return EngagementResponse(True, [], {'engagement':total})

