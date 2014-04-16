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
    entities = fb.entities_to_topics(search_keys)
    
    logging.warning("Search entities: " + str(entities))
    
    recs = rec.recommend_n_friends(3, entities, ["1000"])
    return recs
