import social_networks_term_inspector
from social_networks_term_inspector import EngagementAPI
# from social_networks_term_inspector2 import EngagementTwitterAPI


# from social_networks_term_inspector2 import EngagementAPI

def findInAllAPIsByTerm(query):
    response = EngagementAPI.getEngagement(query.term, useTikTok=False)
    return {
        'term': query.term,
        'twitter': response['twitter'].data['engagement']
    }

