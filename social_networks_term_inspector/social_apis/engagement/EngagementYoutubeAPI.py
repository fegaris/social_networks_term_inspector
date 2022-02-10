import urllib3
import json
from response.EngagementResponse import *
import credentials

key = credentials.KEY
http = urllib3.PoolManager()
class YoutubeAPI:
    def getEngagement(self, search):
        try:
            r = http.request('GET', 'https://www.googleapis.com/youtube/v3/search?maxResults=20&q=' + search + '&type=channel&key=' + key)
            if r.status != 200:
                raise Exception(r.data)
            jsonSearch = json.loads(r.data)
            channel = jsonSearch['items'][0]
            idChannel = channel['id']['channelId']
            r = http.request('GET', 'https://www.googleapis.com/youtube/v3/channels?id=' + idChannel + '&part=snippet,id,brandingSettings,contentDetails,statistics,topicDetails&key=' + key)
            if r.status != 200:
                raise Exception(r.data)
            jsonChannel = json.loads(r.data)
            subscriberCount = int(jsonChannel['items'][0]['statistics']['subscriberCount'])
            channel['info'] = jsonChannel
            channel['engagement'] = self.calculateEngagement(idChannel, subscriberCount)
            return EngagementResponse(True, [], channel)
        except Exception as e:
            return EngagementResponse(True, [e], {})

    def calculateEngagement(self, idChannel, subscriberCount):
        r = http.request('GET', 'https://www.googleapis.com/youtube/v3/search?key=' + key + '&channelId=' + idChannel + '&part=snippet,id&order=date&maxResults=20')
        jsonSearch = json.loads(r.data)
        videos = jsonSearch['items']
        statistics = {
            "viewCount": 0,
            "likeCount": 0,
            "favoriteCount": 0,
            "commentCount": 0,
            "subscriberCount": subscriberCount
        }
        engagement = 0
        for index, video in enumerate(videos):
            if "videoId" in video['id']:
                r = http.request('GET', 'https://www.googleapis.com/youtube/v3/videos?id=' + video['id']['videoId'] + '&part=statistics&key=' + key)
                if r.status != 200:
                    raise Exception(r.data)
                jsonVideo = json.loads(r.data)
                if  'viewCount' in jsonVideo['items'][0]['statistics']:
                    statistics['viewCount'] += int(jsonVideo['items'][0]['statistics']['viewCount'])
                if  'likeCount' in jsonVideo['items'][0]['statistics']:
                    statistics['likeCount'] += int(jsonVideo['items'][0]['statistics']['likeCount'])
                if  'favoriteCount' in jsonVideo['items'][0]['statistics']:
                    statistics['favoriteCount'] += int(jsonVideo['items'][0]['statistics']['favoriteCount'])
                if  'commentCount' in jsonVideo['items'][0]['statistics']:
                    statistics['commentCount'] += int(jsonVideo['items'][0]['statistics']['commentCount'])
                engagement += (statistics['likeCount'] + statistics['commentCount']) / statistics['subscriberCount']
        meanEngagement = engagement / len(videos)
        return meanEngagement