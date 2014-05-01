import requests
import json
from agent_app.models import *

#Assume that the token is good
def get_friend_names(accessToken):
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    js = r.json()
    friends = js['data']
    
    
    names = ''
    for friend in friends:
        #names += '<p>' + friend['name'] + ' ' + str(friend) + '</p>'
        r2 = requests.get('https://graph.facebook.com/' + str(friend['id']), params=payload)
        friend_dict = r2.json()
        
        if 'hometown' in friend_dict:
            names += '<p>' + (r2.json()['name']).encode('utf-8') + ": " + (r2.json()['hometown']['name']).encode('utf-8') + '</p>'
    return names

def num_updated(friends_ids):
    count = 0
    #Could probably have a more efficient query here
    for friend_id in friends_ids:
        s = User.objects.filter(facebook_id = friend_id)
        count += len(s)
    return count


def num_friends(friends_ids):
    logging.warning("test")
    count = 0
    logging.warning("Gets to the num_friends")
    for friend_id in friends_ids:
        s = User.objects.filter(facebook_id = friend_id)
        count += len(s)
    return count
