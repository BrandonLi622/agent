#!/usr/bin/env python
import os
import string
import requests
import json
import logging

from agent_app.models import SiteInteraction, Profile, User
import agent_app.recommender as rec
import agent_app.FB_Utilities as FB_Utilities
import agent_app.freebase as fb


#Assuming search_keys is a list of strings
def recommend(search_keys):
    logging.warning("in recommend")
    mid_tuples = fb.entities_to_mid_tuples(search_keys)
    logging.warning("Search entities: " + str(mid_tuples))
    recs = rec.recommend_n_friends(10, mid_tuples, ["1000", "2000"])
    return recs

def num_updated_friends(user_id):
    logging.warning("User's id: " + str(user_id))
    friends_ids = ['1000', '2000']
    #should really get all of the ids of user_id' friends
    return FB_Utilities.num_updated(friends_ids)
