'''
Agent
 Copyright (c) 2014
 Brandon Li, Daniel Tahara, and Christopher Zeng
 All Rights Reserved.
 NOTICE:  All information contained herein is, and remains
 the property of the above authors The intellectual and technical
 concepts contained herein are proprietary to the authors and
 may be covered by U.S. and Foreign Patents, patents in process,
 and are protected by trade secret or copyright law. Dissemination
 of this information or reproduction of this material is strictly
 forbidden unless prior written permission is obtained from
 the authors.
'''

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
from django.views.decorators.cache import never_cache

def why_recommended(request):
    logging.warning(str(request.GET['friend_id']))
    
    friend_id = request.GET['friend_id']
    search_string = request.GET['query']
    access_token = request.GET['access_token']
    query_type = request.GET['QueryType']

    search_keys = Yahoo_Utilities.extract_entities(search_string)
    mid_tuples = fb.entities_to_mid_tuples(search_keys)
    reasons = rec.why_recommended(mid_tuples, friend_id, access_token, query_type)
    
    logging.warning("Got past reasons")
    
    t = loader.get_template('ReasonResults.html')
    c = Context({
        'post_list': reasons,
        'search_string' : search_string,
    })
    
    html = t.render(c)
    logging.warning("Result html")
    logging.warning(html)
    
    return HttpResponse(html)


def refresh_data(request):
    access_token = ""
    try:
        access_token = request.GET['access_token']
    except KeyError:
        pass
    FB_Utilities.scrape_friend_data(access_token)
    return HttpResponse("")


#This is a hack
def tests(request):
    user2 = User.objects.all().filter(facebook_id = "100000661170750")[0]
    
    fb.add_profile(user2,"Quotes",["turkey"])
    return HttpResponse("hello")
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

@never_cache
def ajax_search(request):
    #logging.disable(logging.CRITICAL)

    search_string= ""
    query_type = ""
    rec_list= []
    access_token=""
    user_id = 0
    num_friends = 0
    logging.warning("Hello there")

    try:
        access_token = request.GET['access_token']
        logging.warning(access_token)

        logging.warning("After scrape")
        
        search_string = request.GET['query']
        query_type = request.GET['QueryType']
        logging.warning(request.GET['user_id'])
        user_id = int(request.GET['user_id'])
        
        logging.warning(query_type)

        #Need to break up the search_string into multiple entities using Yahoo
        #for now just use this
        #search_keys = [search_string]
        search_keys = Yahoo_Utilities.extract_entities(search_string)
        
        logging.warning("Did a search: " + search_string);
        rec_list = integrated.recommend(access_token, search_keys, query_type)
    
    except Exception as e:
        logging.warning("Exception in the view: " + str(e))
    
    num_friends = integrated.num_updated_friends(access_token, user_id)

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

@never_cache
def ajax_aboutpage(request):
    return HttpResponse(loader.get_template('About.html'));

def bad_address(request):
    return HttpResponseRedirect('../agent')
