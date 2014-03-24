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
        names += '<p>' + friend['name'] + ' ' + str(friend) + '</p>'
        r2 = requests.get('https://graph.facebook.com/' + str(friend['id']), params=payload)
        names += '<p>' + str(r2.json()) + '</p>'
    return names