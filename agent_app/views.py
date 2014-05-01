# Create your views here.
import os
import string
import requests
import json
import logging


from django.template import Context, loader

from agent_app.models import SiteInteraction, Profile, User
import agent_app.recommender as rec
import agent_app.FB_Utilities as FB_Utilities
import agent_app.freebase as fb
import agent_app.integrated as integrated
import agent_app.Yahoo_Utilities as Yahoo_Utilities
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#This is a hack
def tests(request):
    user2 = User.objects.all().filter(facebook_id = "2000")[0]
    fb.add_profile(user2,"Quotes",["turkey"])
    
    '''
    entities = fb.entities_to_topics(["apple", "cherry", "mango"])
    html = ""
    for i in entities:
        parent_mid = fb.get_type_mid(i)
        html = html + "<p>" + str(i) + "AND" + str(parent_mid) + "</p>"
    '''
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

def search(request):
    search_string= ""
    rec_list= []
    access_token=""
    
    #user = User.objects.all().filter(facebook_id = "2000")[0]
    #fb.add_profile(user,"Interests",["Italy", "mangoes"])

    
    logging.warning("Hello there")

    try:
        search_string = request.GET['query']
        access_token = request.GET['access_token']
        
        #Need to break up the search_string into multiple entities using Yahoo
        #for now just use this
        #search_keys = [search_string]
        search_keys = Yahoo_Utilities.extract_entities(search_string)

        logging.warning("Did a search: " + search_string);
        rec_list = integrated.recommend(search_keys)
    
    #f = open(os.path.join(os.path.dirname(__file__), 'FB-Login.html'), 'r')
    #html = f.read()
    except Exception:
        pass
    
    num_friends = "27"
    
    t = loader.get_template('FB-Login.html')
    c = Context({
        'rec_list': rec_list,
        'search_string' : search_string,
        'access_token' : access_token,
        'n_friends' : num_friends
    })

    logging.warning(str(rec_list))
    
    return HttpResponse(t.render(c))

def ajax_search(request):
    search_string= ""
    rec_list= []
    access_token=""
    user_id = 0
    logging.warning("Hello there")

    try:
        access_token = request.GET['access_token']
        search_string = request.GET['query']
        user_id = int(request.GET['user_id'])

        #Need to break up the search_string into multiple entities using Yahoo
        #for now just use this
        #search_keys = [search_string]
        search_keys = Yahoo_Utilities.extract_entities(search_string)
        
        logging.warning("Did a search: " + search_string);
        rec_list = integrated.recommend(search_keys)
    
    #f = open(os.path.join(os.path.dirname(__file__), 'FB-Login.html'), 'r')
    #html = f.read()
    except Exception:
        pass
    
    logging.warning("user id is: " + str(user_id))
    num_friends = integrated.num_updated_friends(user_id)
    
    
    t = loader.get_template('SearchResults.html')
    c = Context({
        'rec_list': rec_list,
        'search_string' : search_string,
        'access_token' : access_token,
        'n_friends' : num_friends

    })

    logging.warning(str(rec_list))
    
    return HttpResponse(t.render(c))

def fb_login(request):
    logging.warning("Did a log-in");

    rec_list = []
    
    t = loader.get_template('FB-Login.html')
    c = Context({
        'rec_list': rec_list,
    })
    
    return HttpResponse(t.render(c))

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

def ajax_aboutpage(request):
    return HttpResponse(loader.get_template('About.html'));

def bad_address(request):
    return HttpResponseRedirect('../agent')
