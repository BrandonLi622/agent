import requests
import json

#Assume that the token is good
def get_friend_names(accessToken):
    payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    js = r.json()
    friends = js['data']
    
    
    names = ''
    for friend in friends:
        names += '<p>' + friend['name'] + '</p>'
    return names