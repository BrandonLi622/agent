import json
import urllib
import re
import agent_app.models

# TODO:
# - Error handling for topic/search
# - EAFP (easier to ask forgiveness than permission) > LBYL (look
# before you leap)

API_KEY = "AIzaSyDK5SOekp6eUTSKUfeLiFXv_Qwbbf1csZU"

SEARCH_URL = 'https://www.googleapis.com/freebase/v1/search'
TOPICS_URL = 'https://www.googleapis.com/freebase/v1/topic'

FREEBASE_MID_REGEX = r'^\/m\/\w+$'

def add_interaction(user_id, source_type, entities,
        site_name='facebook'):
    '''Store a given interaction represented by a facebook user_id, source type
    (class name), and list of entities'''

    freebase_topics = entities_to_freebase_topics(entities)
    for topic in freebase_topics:
        mid = topic['mid']
        id = topic['id']
        name = topic['name']

        notable_type = topic['notable']['id']
        if re.search(FREEBASE_MID_REGEX, notable_type):
            # The 'notable' field was a related entity, so look
            # up the original entity and extract notable type
            topic = get_freebase_topic(mid)
            notable_types = topic['property']['/common/topic/notable_types']['values']
            if len(notable_types) == 0:
                notable_type = None
            else:
                notable_type = notable_types[0]['id']

        type = freebase_id_to_mid(notable_type)
        notable_domain = '/' + notable_type.split('/')[1]
        domain = freebase_id_to_mid(notable_domain)

        # Create object of type source type
        interaction = source_type(user_id=user_id,
                site_name=site_name, freebase_mid=mid,
                freebase_id=id, freebase_name=name,
                freebase_type=type, freebase_domain=domain)
        interaction.save()

def entities_to_freebase_topics(entities):
    '''Given a string of tags, return a list of freebase search response
    objects corresponding to those tags'''

    freebase_topics = []
    for entity in entities:
        results = search_freebase(entity)
        if len(results) == 0:
            continue

        # For now, only consider first result
        best_match = results[0]
        freebase_topics.append(best_match)

    return freebase_topics

def freebase_id_to_mid(id):
    topic = get_freebase_topic(id)
    if topic is None:
        return None

    mids = topic['property']['/type/object/mid']['values']
    if len(mids) == 0:
        return None
    else:
        return mids[0]['text']

def search_freebase(query):
    if query is None:
        return None

    params = { 'query': entity, 'key': API_KEY }
    url = SEARCH_URL + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    results = response['result']

    return results

def get_freebase_topic(query):
    '''Takes a mid or id and returns associated topic'''
    if query is None:
        return None

    params = { 'key': API_KEY }
    url = TOPICS_URL + query + '?' +  urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    return response
