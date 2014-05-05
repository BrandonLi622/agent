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

#!/usr/bin/env python
import os
import string
import requests
import json
import logging
import random
#logging.disable(logging.CRITICAL)

from agent_app.models import SiteInteraction, Profile, User
import agent_app.recommender as rec
import agent_app.FB_Utilities as FB_Utilities


import agent_app.freebase as fb


#Assuming search_keys is a list of strings
def recommend(access_token, search_keys, query_type):
    logging.warning("in recommend")
    logging.warning("search keys: " + str(search_keys))
    mid_tuples = fb.entities_to_mid_tuples(search_keys)
    logging.warning("Search entities: " + str(mid_tuples))
    friend_ids = FB_Utilities.get_friend_ids(access_token)
    
    final_friend_ids = []
    for friend_id in friend_ids:
        try:
            User.objects.get(facebook_id = friend_id)
            final_friend_ids.append(friend_id)
        except Exception as e:
            continue
    
    logging.warning("Final friend ids: " + str(final_friend_ids))
    
    random.shuffle(final_friend_ids)
    
    recs = rec.recommend_n_friends(10, mid_tuples, final_friend_ids, query_type)
    return recs

def num_updated_friends(access_token, user_id):
    logging.warning("User's id: " + str(user_id))
    friends_ids = FB_Utilities.get_friend_ids(access_token)
    #should really get all of the ids of user_id' friends
    return FB_Utilities.num_updated(friends_ids)
