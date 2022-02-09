#from asyncio.windows_events import NULL
#from urllib import response
#from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from services import APIHub
@csrf_exempt
def index(request):
    response = {}
    if(request.POST):
        query = type('',(object,),{
            'term': request.POST.get('searchTerm'),
            'useTwitter': request.POST.get('useTwitter'),
            'useLinkedIn': request.POST.get('useLinkedIn'),
            'useInstagram': request.POST.get('useInstagram'),
            'useTikTok': request.POST.get('useTikTok'),
            'useYoutube': request.POST.get('useYoutube'),
            'useTwich': request.POST.get('useTwich'),
         })()
        response = APIHub.findInAllAPIsByTerm(query)
    return render(request, 'index.html', {'response':response})
    

        

