import json
import urllib
import re
from agent_app.models import *
import logging

# TODO:
# - Error handling for topic/search
# - EAFP (easier to ask forgiveness than permission) > LBYL (look
# before you leap)

API_KEY = "AIzaSyDK5SOekp6eUTSKUfeLiFXv_Qwbbf1csZU"

SEARCH_URL = 'https://www.googleapis.com/freebase/v1/search'
TOPICS_URL = 'https://www.googleapis.com/freebase/v1/topic'

FREEBASE_MID_REGEX = r'^\/m\/\w+$'

#takes a freebase entity and returns its parent's mid
#-Brandon
def get_notable_type(topic):
    mid = topic['mid']
    id = topic['id']
    name = topic['name']
    
    notable_type = topic['notable']['id']
                
    if re.search(FREEBASE_MID_REGEX, notable_type):
    # The 'notable' field was a related entity, so look
    # up the original entity and extract notable type
        topic = get_topic(mid)
        notable_types = topic['property']['/common/topic/notable_types']['values']
        if len(notable_types) == 0:
            notable_type = None
        else:
            notable_type = notable_types[0]['id']

    return notable_type

def get_type_mid(topic):
    return id_to_mid(get_notable_type(topic))

def get_domain_mid(topic):
    notable_type = get_notable_type(topic)
    notable_domain = '/' + notable_type.split('/')[1]
    domain = id_to_mid(notable_domain)
    return domain


def add_count(topic):
    mid = topic['mid']
    tf, is_created = TermFrequency.objects.get_or_create(freebase_mid = mid)

    logging.warning(str(tf))
    tf.freq_count = tf.freq_count + 1
    
    logging.warning("Adding count: " + str(tf.freq_count))
    tf.save()
    
def add_counts(topics):
    for topic in topics:
        add_count(topic)

def add_interaction(user, source_type, entities,
        site_name='facebook'):
    '''Store a given interaction represented by a facebook user_id, source type
    (class name), and list of entities'''

    topics = entities_to_topics(entities)
    for topic in topics:
        mid = topic['mid']
        id = topic['id']
        name = topic['name']
        notable_type = get_notable_type(topic) #id_to_mid(notable_type)
        type = id_to_mid(notable_type)
        domain = get_domain_mid(topic)

        # Create object of type source type
        interaction = source_type(user_id=user,
                site_name=site_name, freebase_mid=mid,
                freebase_id=id, freebase_name=name,
                freebase_type=type, freebase_domain=domain)
        interaction.save()

def entities_to_topics(entities):
    '''Given a string of tags, return a list of freebase search response
    objects corresponding to those tags'''

    topics = []
    for entity in entities:
        results = search(entity)
        if len(results) == 0:
            continue

        # For now, only consider first result
        best_match = results[0]
        topics.append(best_match)

    return topics

def id_to_mid(id):
    topic = get_topic(id)
    if topic is None:
        return None

    #logging.warning(str(topic))

    mids = topic['property']['/type/object/mid']['values']
    if len(mids) == 0:
        return None
    else:
        return mids[0]['text']

def search(query):
    if query is None:
        return None

    params = { 'query': query, 'key': API_KEY }
    url = SEARCH_URL + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())    
    results = response['result']

    return results

def get_topic(query):
    '''Takes a mid or id and returns associated topic'''
    if query is None:
        return None

    params = { 'key': API_KEY }
    url = TOPICS_URL + query + '?' +  urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    #logging.warning(query)
    #logging.warning(str(response))


    return response
