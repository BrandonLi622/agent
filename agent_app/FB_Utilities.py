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

import random
import requests
import logging
import json
import agent_app.freebase as fb
import agent_app.Yahoo_Utilities as Yahoo_Utilities
from agent_app.models import *
#logging.disable(logging.CRITICAL)

#Assume that the token is good
def get_friend_ids(accessToken):
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    js = r.json()
    friends = js['data']

    ids = []
    if friends is not None:
        for friend in friends:
            ids.append(friend['id'])
            
    logging.warning("getting ids")

    return ids


def get_friend_names(accessToken):
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    js = r.json()
    friends = js['data']
    names = ''
    if friends is not None:
    	for friend in friends:
    	    names += '<p>' + friend['name'] + '<//p>'
    return names

def retrieve_facebook_item(url, type, accessToken):
    payload = {'access_token': accessToken}
    #r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    r = requests.get(url, params=payload)
    try:
        if type == "hometown":
            data = r.json()['data'][0]
            reason = "Hometown: " + data
        elif type == "like":
            data = r.json()['data'][0]['name']
            reason = "Likes: " + data
            return reason
        elif type == "status":
            data = r.json()['message']
            reason = "Status: " + data
            return reason
        else:
            return str(data)
    except Exception as e:
        logging.warning("Exception in retrieve_facebook_item: " + str(e))
        return ""


def scrape_friend_data(accessToken):
    logging.warning("start_function")
    logging.warning("access token is: " + accessToken)
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends/', params=payload)
    js = r.json()
    logging.warning("js is: " + str(js))
    friends = js['data']
    random.seed()


    FriendData = []
    #i = 1
    #for friend in friends:
    for i in range(0,len(friends)):
        try:
            friend = friends[i]#[random.randint(0,len(friends)-1)]
            name = friend['name']
            logging.warning(str(User.objects.all()))
            logging.warning("check")
            if len(User.objects.all().filter(facebook_id = friend['id'])) == 0:
                logging.warning("!!" + name)
                user = User(facebook_id=friend['id'], facebook_name=name)
                user.save()
                data = []
                #logging.warning(str(i ) + " " + name + " " + friend['id'])
                i=i+1
                r2 = requests.get('https://graph.facebook.com/' + str(friend['id']), params=payload)
                friend_dict = r2.json()
                if 'hometown' in friend_dict:
                    hometown = friend_dict['hometown']['name']
                    logging.warning("Adding hometown")
                    fb.add_profile(user,'hometown', 'Hometown: ' + hometown, [hometown])
                    #fb.add_interaction(friend['id'], 'hometown', [hometown], "Profile")
                    data.append(hometown)	
    
                r3 = requests.get('https://graph.facebook.com/' + str(friend['id']) + '/likes', params=payload)
                likes_dict = r3.json()['data']
                
                logging.warning(str(len(likes_dict)))
                for like in likes_dict:
                    try:
                        likeid = str(like['id'])
                        likename = str(like['name'])
                        
                        retrieve_url = 'https://graph.facebook.com/' + str(friend['id']) + '/likes/' + likeid
                        
                        fb.add_action(user,'like',retrieve_url,[likename])
                        data.append(likename)
                    except Exception as e:
                        logging.warning(str(e))
                        pass
    
                r4 = requests.get('https://graph.facebook.com/' + str(friend['id']) + '/statuses', params=payload)
                logging.warning("Getting to statuses?")
                logging.warning(str(r4.json()))

                status_dict = r4.json()['data']
                logging.warning(str(status_dict))
                logging.warning(str(len(status_dict)))
                for status in status_dict:
                    try:
                        statusid = status['id']
                        retrieve_url = 'https://graph.facebook.com/' + statusid
                        resultlist = Yahoo_Utilities.extract_entities(status['message'])
                        fb.add_action(user,'status',retrieve_url,resultlist)
                    except Exception as e:
                        logging.warning(str(e))
                        pass
        except Exception as e:
            logging.warning("Exception in scraping: " + str(e))

def num_updated(friends_ids):
    count = 0
    #Could probably have a more efficient query here
    for friend_id in friends_ids:
        s = User.objects.filter(facebook_id = friend_id)
        count += len(s)
    logging.warning("made it to end of function")
    return count

