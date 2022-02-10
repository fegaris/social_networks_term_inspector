from response.EngagementResponse import *

class APIExample:
    def getEngagement(user):
        ## Hacemos la llamada a la API correspondiente, realizamos los calculos 
        # necesarios y devolvemos el objeto EngagementResponse con los valores
        return EngagementResponse(True, [], {'engagement':'15'})


#print(APITwitter.getEngagement('Auron'))
response = APIExample.getEngagement('Auron')
print(response.data['engagement'])