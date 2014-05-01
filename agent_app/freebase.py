import json
import urllib
import re
from agent_app.models import *
import logging
from datetime import datetime, date

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
    logging.warning("topic is")
    id = None
    try:
        id = topic['id']
    except KeyError:
        pass
    name = topic['name']
    logging.warning("topic is")


    notable_type = None
    try:
        logging.warning("Does it get here?")
        notable_type = topic['notable']['id']
    except KeyError:
        pass
    except Exception:
        logging.warning("Different exception")
        pass

    logging.warning("marker")

    # This is really shitty code; this should probably be wrapped in the
    # try/except somehow with a custom execption
    if notable_type is None or re.search(FREEBASE_MID_REGEX, notable_type):
    # The 'notable' field was a related entity, so look
    # up the original entity and extract notable type
        topic = get_topic(mid)
        #logging.warning("topic is: " + str(topic))
        
        notable_types = []
        try:
            notable_types = topic['property']['/common/topic/notable_types']['values']
        except KeyError:
            pass

        if len(notable_types) == 0:
            types = topic['property']['/type/object/type']['values']
            if len(types) == 0:
                notable_type = None
            else:
                notable_type = types[0]['id']
        else:
            notable_type = notable_types[0]['id']
    logging.warning("Notable type is: " + "test")
    return notable_type

def get_type_mid(topic):
    return id_to_mid(get_notable_type(topic))

def get_domain_mid(topic):
    notable_type = get_notable_type(topic)
    notable_domain = '/' + notable_type.split('/')[1]
    domain = id_to_mid(notable_domain)
    return domain

def add_count(mid_tuple):
    mid = mid_tuple[0]
    tf, is_created = TermFrequency.objects.get_or_create(freebase_mid = mid)

    logging.warning(str(tf))
    tf.freq_count = tf.freq_count + 1
    
    logging.warning("Adding count: " + str(tf.freq_count))
    tf.save()
    
def add_counts(mid_tuples):
    for mid_tuple in mid_tuples:
        add_count(mid_tuple)

#should this really be add interactions?
def add_profile(user, field_type, entities,
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
        interaction = Profile(user_id=user,
                site_name=site_name, freebase_mid=mid,
                freebase_id=id, freebase_name=name,
                freebase_type=type, freebase_domain=domain, field_type=field_type)
        interaction.save()

#should this really be add interactions?
def add_action(user, field_type, field_id, entities,
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
        interaction = Action(user_id=user,
                site_name=site_name, freebase_mid=mid,
                freebase_id=id, freebase_name=name,
                freebase_type=type, freebase_domain=domain,
                field_type=field_type, field_id = field_id)
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
        mid = best_match['mid']
        topics.append(best_match)

    return topics

def entities_to_mid_tuples(entities):
    all_tuples = []
    for entity in entities:
        results = search(entity)

        if len(results) == 0:
            continue
        # For now, only consider first result
        best_result = results[0]
        mid = best_result['mid']
        #topic = get_topic(mid)
        #best_result['id'] = topic['id']

        mid_tuples = FreebaseMids.objects.filter(mid = mid)
        logging.warning("hello there from freebase")
        logging.warning("test " + str(len(mid_tuples)))

        type_mid = ""
        domain_mid = ""
    
        if len(mid_tuples) == 0:
            logging.warning("Entered get mid tuple")
            #logging.warning("best result" + str(best_result))
            type_mid = get_type_mid(best_result)
            domain_mid = get_domain_mid(best_result)
            new_mid_tuple = FreebaseMids(search_key=entity, mid=mid,
                                         type_mid = type_mid,
                                         domain_mid = domain_mid)
            new_mid_tuple.save()
            logging.warning("Finished saving")
        else:
            logging.warning("Entered else condition")
            cached_result = mid_tuples[0]
            logging.warning("Cached result: " + str(cached_result))
            mid = cached_result.mid
            type_mid = cached_result.type_mid
            domain_mid = cached_result.domain_mid
            logging.warning("Got cached result")
        
        logging.warning(mid + " sep " + type_mid + " sep " + domain_mid)
        new_tuple = (mid, type_mid, domain_mid)
        all_tuples.append(new_tuple)
        logging.warning("Finished iteration of loop")

    logging.warning("All tuples: " + str(all_tuples))
    return all_tuples

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
    logging.warning("called url " + url)
    
    starttime = datetime.now()
    response = json.loads(urllib.urlopen(url).read())
    endtime = datetime.now()
    logging.warning("Request duration " + str(endtime - starttime))


    #logging.warning(query)
    #logging.warning(str(response))


    return response
