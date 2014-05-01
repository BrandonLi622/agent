import requests
import json
import logging
import agent_app.freebase as fb

#Assume that the token is good
def get_friend_names(accessToken):
	payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends', params=payload)
    #q = 'SELECT+uid,+name,+interests+FROM+user+WHERE+uid+IN+(SELECT+uid2+FROM+friend+WHERE+uid1+=+me())'
    #q = 'SELECT+uid2+FROM+friend+WHERE+uid1+=+me()'
    #r = requests.get('https://graph.facebook.com/fql?q='+q, params=payload)
    js = r.json()
    friends = js['data']
    
    names = ''
    if friends is not None:
    	for friend in friends:
    		names += '<p>' + friend['name'] + '<//p>'
	return names
    #return str(js)
    #payload = {'access_token': accessToken}
    #q = 'SELECT+uid2+FROM+friend+WHERE+uid1+=+me()'
    #r = requests.get('https://graph.facebook.com/fql?q='+q, params=payload)
    #js = r.json()
    #logging.warning(str(js))
    #return str(js)
    

def scrape_friend_data(accessToken):
	payload = {'access_token': accessToken}
    r = requests.get('https://graph.facebook.com/me/friends/', params=payload)
    js = r.json()
    friends = js['data']
    

    FriendData = []
    i = 1
    for friend in friends:
        name = friend['name']
        data = [];
        #logging.warning(str(i ) + " " + name)
    	i=i+1
        r2 = requests.get('https://graph.facebook.com/' + str(friend['id']), params=payload)
        friend_dict = r2.json()
        if 'hometown' in friend_dict:
            hometown = friend_dict['hometown']
            data.append(hometown['name'])
        r3 = requests.get('https://graph.facebook.com/' + str(friend['id'] + "/likes"), params=payload)
        likes_dict = r3.json()['data']
        #logging.warning(likes_dict)
        for like in likes_dict:
        	#logging.warning(like['name'])
        	try:
        		likename = str(like['name'])
        		data.append(likename)
        	except:
        		pass

		
    	#logging.warning("DATA" + str(data))
    	entities = []
    	if len(data) > 0:
    		entities = fb.entities_to_topics(data)
    	#logging.warning("ENTITIES" + str(entities))
        #FriendData.append([name,entities])
    	if i > 10:
			break

    return FriendData
