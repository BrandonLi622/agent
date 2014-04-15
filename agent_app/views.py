# Create your views here.
import os
import string
import requests
import json

from agent_app.models import SiteInteraction, Profile, User
import agent_app.recommender as rec
import agent_app.FB_Utilities as FB_Utilities
import agent_app.freebase as fb
import agent_app.integrated as integrated
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#This is a hack
def tests(request):
    entities = fb.entities_to_topics(["apple", "cherry", "mango"])
    html = ""
    for i in entities:
        parent_mid = fb.get_type_mid(i)
        html = html + "<p>" + str(i) + "AND" + str(parent_mid) + "</p>"
    
    #hardcoded test
    #user = User.objects.all().filter(facebook_id = "1000")[0]
    #fb.add_interaction(user,Profile,["apple", "cherry", "mango"])
    #entries = rec.get_friend_entries("1000")
    #entities = fb.entities_to_topics(["cherry"])
    #friend_score = rec.score_friend([entity], "1000")
    #recs = rec.recommend_n_friends(3, entities, ["1000"])
    
    search_keys = ["cherry"]
    recs = integrated.recommend(search_keys)
    
    #score = rec.score_entity(entity, entries)
    html = html + "<p>Entity is: " + str(entities[0]) + "</p>"
    
    html = html + "<p>Recs are:</p>"
    index = 1
    for r in recs:
        html = html + "<p>" + str(index) + ": " + r + "</p>"
        index += 1
    
    return HttpResponse(html)


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