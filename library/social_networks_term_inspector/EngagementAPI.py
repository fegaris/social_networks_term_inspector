from . import EngagementTwitterAPI
from . import APITikTok


# from EngagementTwitterAPI import APITwitter


def getEngagement(user, useTwitter=True, useTikTok=True):
    twitter = ''
    tiktok = ''

    if useTwitter:
        twitter = EngagementTwitterAPI.getEngagement(user)

    if useTikTok:
        tiktok = APITikTok.getEngagement(user)

    return {
        'twitter': twitter,
        'tiktok': tiktok
    }
