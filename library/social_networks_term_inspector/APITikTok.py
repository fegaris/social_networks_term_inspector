from . import credentials
from .EngagementResponse import EngagementResponse
from TikTokApi import TikTokApi
#pip install git+https://github.com/Daan-Grashoff/TikTok-Api
#(Número de me gusta + número de comentarios + número de veces compartido) / número de visualizaciones) * 100%
def getEngagement(usuario):

    api = TikTokApi.get_instance(custom_verifyFp=credentials.verifyFp)
    data = []
    dato=[]
    usern = api.by_username(usuario)

    for tiktok in usern:
        username=tiktok.get('author',{}).get('uniqueId')
        userfollowers=tiktok.get('authorStats',{}).get('followerCount')
        uservideocount = tiktok.get('authorStats', {}).get('videoCount')
        userlikes = tiktok.get('authorStats', {}).get('heartCount')


        data.append({
        'username': username,
        'userfollowers' : userfollowers,
        'uservideocount' : uservideocount,
        'userlikes' : userlikes
        })

    #print(username, userfollowers, uservideocount, userlikes)


    tiktoks = api.by_username(usuario, count=uservideocount)

    for tiktok2 in tiktoks:
        videoviews=tiktok2.get('stats',{}).get('playCount'),
        videosharecount = tiktok2.get('stats', {}).get('shareCount')
        videolikecount = tiktok2.get('stats', {}).get('diggCount')
        videocommentcount = tiktok2.get('stats', {}).get('commentCount')
        videoid = tiktok2.get('id', {})


        dato.append({
        'videoviews' : videoviews,
        'videosharecount' : videosharecount,
        'videolikecount' : videolikecount,
        'videocommentcount' : videocommentcount,
        'videoid' : videoid
        })

    v=0
    s=0
    l=0
    c=0
    #print(dato)
    for i in dato :
        v = v + sum(i['videoviews'])
        s = s + i['videosharecount']
        l = l + i['videolikecount']
        c = c + i['videocommentcount']
    #print(v, s, l, c)
    engagement=str(((s+c+s)/v)*100)
    #print(engagement)
    return EngagementResponse(True, [], {'engagement': engagement})