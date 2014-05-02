import random
import requests
import json
import logging
import agent_app.freebase as fb
import agent_app.Yahoo_Utilities as Yahoo_Utilities
from agent_app.models import *

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
	random.seed()


	FriendData = []
	#i = 1
	#for friend in friends:
	n = 10
	for i in range(0,n):
		friend = friends[random.randint(0,len(friends)-1)]
		name = friend['name']
		logging.warning(User.objects.all())
		if len(User.objects.all().filter(facebook_id = friend['id'])) == 0:
			logging.warning("!!")
			interaction = User(facebook_id=friend['id'], facebook_name=name)
			interaction.save()
			data = []
			#logging.warning(str(i ) + " " + name + " " + friend['id'])
			i=i+1
			r2 = requests.get('https://graph.facebook.com/' + str(friend['id']), params=payload)
			friend_dict = r2.json()
			if 'hometown' in friend_dict:
				hometown = friend_dict['hometown']
				data.append(hometown['name'])	

			r3 = requests.get('https://graph.facebook.com/' + str(friend['id']) + '/likes', params=payload)
			likes_dict = r3.json()['data']
			for like in likes_dict:
				try:
					likeid = str(like['id'])
					likename = str(like['name'])
					data.append(likename)
				except Exception:
					pass

			r4 = requests.get('https://graph.facebook.com/' + str(friend['id']) + '/statuses', params=payload)
			status_dict = r4.json()['data']
			for status in status_dict:
				try:
					statusid = status['id']
					resultlist = Yahoo_Utilities.extract_entities(status['message'])
					for result in resultlist:
						data.append(result)
				except Exception:
					pass



		break



	return FriendData
