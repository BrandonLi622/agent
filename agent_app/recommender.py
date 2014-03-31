#import agent_app.models
import random
import agent_app.freebase as fb
from agent_app.models import SiteInteraction, Profile, User
import logging


#for a friend_id get all of the entries in SiteInteraction associated with it
def get_friend_entries(friend_id):
    
    #should be unique, assume there's an answer
    user = User.objects.all().filter(facebook_id = friend_id)[0]
        
    s = Profile.objects.all().filter(user_id = user)
    return s

#for a given entity, return a score based on the current user
#uses a naive algorithm
#friend_entries is a list of models.SiteInteraction
def score_entity(search_entity, friend_entries):
    score = 0.0
    
    #logging.warning(str(friend_entries))
    #logging.warning(str(search_entity))
    
    #Points for matching mid (or category mid, do it recursively)
    for db_entity in friend_entries:                
        if search_entity['mid'] == db_entity.freebase_mid:
            score += 3.0
            
        #logging.warning(str(db_entity.freebase_type))
        #logging.warning(str(fb.get_type_mid(search_entity)))
        
        #check if this works
        if fb.get_type_mid(search_entity) == db_entity.freebase_type:
            score += 2.0
            
        if fb.get_domain_mid(search_entity) == db_entity.freebase_domain:
            score += 1.0
        
    return score

#For now do a dumb algorithm which involves aggregating
#scores from the different entites
#Returns a list of tuples (friend_id, score)
def score_friend(entity_list, friend_id):
    entity_scores = []
    for i in range(0,len(entity_list)):
        #Probably not the best way to do this, passing a huge argument
        friend_entries = get_friend_entries(friend_id)
        entity_scores.append(score_entity(entity_list[i], friend_entries))
    
    #takes the average score (maybe what we want is the max or something)
    overall_score = reduce(lambda x, y: 1.0 * x + y, entity_scores) / len(entity_scores)
    
    return (friend_id, overall_score)

#friend_list is a list of id's
#entity_list is a list of the actual entities
#returns a list of User ID's
def recommend_n_ids(n, entity_list, friend_list):
    friend_scores=[]
    
    for i in range(0,len(friend_list)):
        friend_scores.append(score_friend(entity_list, friend_list[i]))
    
    friend_scores.sort(key=lambda tup: tup[1], reverse=True)
    top_scores = friend_scores[0:n]
    recommendations = [i[0] for i in top_scores]
    return recommendations

def recommend_n_friends(n, entity_list, friend_list):
    ids = recommend_n_ids(n, entity_list, friend_list)
    logging.warning(str(ids))
    logging.warning(str(User.objects.all().filter(facebook_id = '1000')))
    
    
    recs = [User.objects.all().filter(facebook_id = i)[0].facebook_name for i in ids]
    return recs


#facebook_ids = [1,2,3,4,5]
#entities = fb.entities_to_topics(["apple", "cherry", "mango"])
#recommend_n_friends(3,[1,2,3,4,5,6,7],[1,2,3,4,5])


