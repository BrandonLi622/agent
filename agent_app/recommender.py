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

#import agent_app.models
import random
import agent_app.freebase as fb
from agent_app.models import *
import logging
from django.db.models import Sum
import agent_app.FB_Utilities as FB_Utilities

#logging.disable(logging.CRITICAL)

alpha = 10.0
beta = 2.0
gamma = 1.0

status_scale = 0.1
like_scale = 1.0
profile_scale = 5.0


#for a friend_id get all of the entries in SiteInteraction associated with it
def get_friend_entries(friend_id, entry_type):
    #should be unique, assume there's an answer
    logging.warning("before user")
    user = ""
    try:
        user = User.objects.get(facebook_id = friend_id)
    except Exception as e:
        return []
    logging.warning("passing user")
    if (entry_type == "Profile"):
        logging.warning("entering profile")
        return Profile.objects.filter(user_id = user)
    elif (entry_type == "Action"):
        return Action.objects.filter(user_id = user)
    elif (entry_type == "Location"):
        return Location.objects.filter(user_id = user)

#for a given entity, return a score based on the current user
#uses a naive algorithm
#friend_entries is a list of models.SiteInteraction

#mid_tuple is (mid, type_mid, domain_mid)
def score_entity(mid_tuple, friend_entries, entry_type):
    logging.warning("got into score entity");
    score = 0.0    
    mid = mid_tuple[0]
    type_mid = mid_tuple[1]
    domain_mid = mid_tuple[2]
    
    type_scale = 1.0

    #Points for matching mid (or category mid, do it recursively)
    for db_entity in friend_entries:                
        if mid == db_entity.freebase_mid:
            score += alpha
        elif type_mid == db_entity.freebase_type:
            score += beta
        elif domain_mid == db_entity.freebase_domain:
            score += gamma
    
    #scale the score by how infrequent it is
    #assume entity is in the table because should be added by point of recommend_n_friends
    
    logging.warning("Count: " + str(score))
    
    tf, is_new = TermFrequency.objects.get_or_create(freebase_mid = mid)
    logging.warning("Frequency is: " + str(tf.freq_count))
    
    total_count = TermFrequency.objects.aggregate(Sum('freq_count'))['freq_count__sum']
    
    freq_scaling = 1.0 * (total_count + 1.0) / (int(tf.freq_count) + 1)
    score *= freq_scaling
    
    logging.warning("Frequency scaled score: " + str(score))
    
    return score

#For now do a dumb algorithm which involves aggregating
#scores from the different entites
#Returns a list of tuples (friend_id, score)
def score_friend(mid_tuple_list, friend_id, query_type):
    entity_scores = []
    for i in range(0,len(mid_tuple_list)):
        logging.warning("Scoring an entity: " + str(i))
        logging.warning(str(friend_id))
        #Probably not the best way to do this, passing a huge argument
        
        if query_type == "general":
            friend_entries = get_friend_entries(friend_id, "Profile")
            logging.warning("1")
            entity_scores.append(score_entity(mid_tuple_list[i], friend_entries))
                
            friend_entries = get_friend_entries(friend_id, "Action")
            logging.warning("2")
            entity_scores.append(score_entity(mid_tuple_list[i], friend_entries))
        
        if query_type == "general" or query_type == "location": 
            logging.warning("3")
            friend_entries = get_friend_entries(friend_id, "Location")
            entity_scores.append(score_entity(mid_tuple_list[i], friend_entries))
            logging.warning("5")
    
    logging.warning("Entity scores: " + str(entity_scores))
    
    #Bonus points for more matches
    num_matches = 0
    for e in entity_scores:
        if e > 0.0:
            num_matches += 1
    
    scaling = 1.0 * num_matches / len(entity_scores)
    
    #takes the average score (maybe what we want is the max or something)
    overall_score = scaling * reduce(lambda x, y: 1.0 * x + y, entity_scores) / len(entity_scores)
        
    logging.warning("Final score: " + str(overall_score))
    return (friend_id, overall_score)

'''
def get_mid_tuple(entity):
    logging.warning("entity: " + str(entity)) 
    mids = FreebaseMids.objects.filter(search_key = entity['mid'])
    mid, type_mid, domain_mid
    
    
    if not(mids):
        logging.warning("Entered get mid tuple")

        mid = entity['mid']
        type_mid = fb.get_type_mid(entity)
        domain_mid = fb.get_domain_mid(entity)
        new_mid_tuple = FreebaseMids(search_key=entity, mid=mid, type_mid = type_mid, domain_mid = domain_mid)
        new_mid_tuple.save()
        logging.warning("Finished saving")
    else:
        cached_result = mids[0]
        mid = cached_result['mid']
        type_mid = cached_result['type_mid']
        domain_mid = cached_result['domain_mid']
        logging.warning("Got cached result")
    return mid, type_mid, domain_mid
'''

#friend_list is a list of id's
#entity_list is a list of the actual entities
#returns a list of User ID's
def recommend_n_ids(n, mid_tuple_list, friend_list, query_type):
    friend_scores=[]
    logging.warning("mid_tuple_list" + str(mid_tuple_list))
                    
    for i in range(0,len(friend_list)):
        logging.warning("Going through loop: " + str(i))
        friend_scores.append(score_friend(mid_tuple_list, friend_list[i], query_type))
    
    friend_scores.sort(key=lambda tup: tup[1], reverse=True)
    top_scores = friend_scores[0:n]
    logging.warning(str(top_scores))
    
    ids = [i[0] for i in top_scores]
    scores = [i[1] for i in top_scores]
    return ids, scores

def recommend_n_friends(n, mid_tuple_list, friend_list, query_type):
    #should I do this here or elsewhere?
    
    #NOTE: This really should be topic list
    fb.add_counts(mid_tuple_list)
    
    logging.warning("Starting recommendations: " + query_type)
    (ids, scores) = recommend_n_ids(n, mid_tuple_list, friend_list, query_type)
    
    logging.warning(str(ids))
    
    logging.warning("My recommendations:" + str(ids))
    #TODO: FIX THIS, not all friends in the database
    recs = [User.objects.get(facebook_id = i).facebook_name for i in ids]
    logging.warning("My recommendations:" + str(recs))

    
    #Returns both the names and the id's, so that we can visit their pages
    return zip(recs, ids, scores)

def find_top_entities(mid_tuple, friend_entries):
    scores = []  
    mid = mid_tuple[0]
    type_mid = mid_tuple[1]
    domain_mid = mid_tuple[2]

    for db_entity in friend_entries:                
        if mid == db_entity.freebase_mid:
            scores.append((db_entity, alpha))
        elif type_mid == db_entity.freebase_type:
            scores.append((db_entity, beta))
        elif domain_mid == db_entity.freebase_domain:
            scores.append((db_entity, gamma))
    return scores

def show_score_friend(mid_tuple_list, friend_id, query_type):
    entity_scores = []
    for i in range(0,len(mid_tuple_list)):
        logging.warning("Scoring an entity: " + str(i))
        logging.warning("Friend id: " + friend_id)
        #Probably not the best way to do this, passing a huge argument
        
        if query_type == "general":
            friend_entries = get_friend_entries(friend_id, "Profile")
            entity_scores += find_top_entities(mid_tuple_list[i], friend_entries)
    
            friend_entries = get_friend_entries(friend_id, "Action")
            entity_scores += find_top_entities(mid_tuple_list[i], friend_entries)

        if query_type == "general" or query_type == "location":
            friend_entries = get_friend_entries(friend_id, "Location")
            entity_scores += find_top_entities(mid_tuple_list[i], friend_entries)
        
    
    score_dict = {}
    types = {}
    posts = []
    type = ""
    for escores in entity_scores:
        url = ""
        try:
            url = escores[0].retrieval_url
            type = escores[0].field_type
            if url == "":
                url = type
                logging.warning("No URL, Type is: " + type)
        except Exception as e:
            logging.warning("Could not get retrieval url")
            continue

        try:
            score_dict[url] += escores[1]
        except Exception as e:
            score_dict[url] = escores[1]
            posts.append(url)
            types[url] = type
            logging.warning("Appending post: " + url)
    
    logging.warning("Done loading scores")

    
    return score_dict, posts, types

def why_recommended(mid_tuple_list, friend_id, accessToken, query_type):
    (results, impt, types) = show_score_friend(mid_tuple_list, friend_id, query_type)
    
    logging.warning("Getting reasons")
    logging.warning(str(results))
    logging.warning("impt: " + str(impt))
    
    scores = [results[i] for i in impt]
    ts = [types[i] for i in impt]
    
    temp = zip(scores, impt, ts)
    temp.sort(key=lambda tup: tup[0], reverse=True)  #sorts in place
    
    reason_pairs = [(t[1], t[2]) for t in temp]
    
    final_reasons = []
    counter = 0
    
    try:
        for reason_pair in reason_pairs:
            reason = str(reason_pair[0])
            type = str(reason_pair[1])
            if 'https' in reason:
                result_string = FB_Utilities.retrieve_facebook_item(reason, type, accessToken)
                if result_string != "":
                    final_reasons.append(result_string)
                    counter += 1
            else:
                final_reasons.append(reason)
                counter += 1
            
            if counter == 5:
                break
    except Exception as e:
        logging.warning("Exception in reason finding: " + str(e))
    return final_reasons  


#facebook_ids = [1,2,3,4,5]
#entities = fb.entities_to_topics(["apple", "cherry", "mango"])
#recommend_n_friends(3,[1,2,3,4,5,6,7],[1,2,3,4,5])


