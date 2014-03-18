# Create your views here.
import os
import string
import requests
import json

import FB_Utilities
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def fb_login(request):
    f = open(os.path.join(os.path.dirname(__file__), 'FB-Login.html'), 'r')
    html = f.read()
    return HttpResponse(html)

def logged_in(request, accessToken):
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/', params=payload)
    f = open(os.path.join(os.path.dirname(__file__), 'Home.html'), 'r')
    html = f.read()
    
    if (r.status_code == 200):
        html = html.replace("<body>", "<body>" + FB_Utilities.get_friend_names(accessToken))
        return HttpResponse(html)
    else:
        #html = html.replace("<body>", "<body>ERROR: " + str(r.status_code))
        #this is just the way that our url is formatted...
        return HttpResponseRedirect('../../agent')
        #return HttpResponse(html)


def bad_address(request):
    return HttpResponseRedirect('../agent')