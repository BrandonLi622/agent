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

from django.db import models

# TODO:
# - Required fields
# - Check field lengths

# Django creates default primary keys:
# https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields

class FreebaseMids(models.Model):
    objects = models.Manager() #Necessary to perform queries
    search_key = models.CharField(max_length=50)
    mid = models.CharField(max_length=50)
    type_mid = models.CharField(max_length=50)
    domain_mid = models.CharField(max_length=50)
    
    def __unicode__(self):
	return self.search_key

class TermFrequency(models.Model):
    objects = models.Manager() #Necessary to perform queries
    
    freebase_mid = models.CharField(max_length=20)
    freq_count = models.IntegerField(default=0)
    
    def __unicode__(self):
	return self.freebase_mid


class User(models.Model):
    objects = models.Manager() #Necessary to perform queries

    facebook_id = models.CharField(primary_key=True, max_length=70)
    facebook_name = models.CharField(max_length=50)
    last_updated = models.DateField(auto_now=True) # New timestamp each time it saves


    def __unicode__(self):
	return self.facebook_name

class SiteInteraction(models.Model):
    user_id = models.ForeignKey(User) # Defaults to DELETE CASCADE
    site_name = models.CharField(max_length=20)
    freebase_mid = models.CharField(max_length=20)
    freebase_id = models.CharField(max_length=100)
    freebase_name = models.CharField(max_length=100)
    freebase_type = models.CharField(max_length=20)
    freebase_domain = models.CharField(max_length=20)
    field_type = models.CharField(max_length=50) #e.g. interests, etc.
    retrieval_url = models.CharField(max_length=1000)

    def __unicode__(self):
	return self.freebase_id

    # See: https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes
    class Meta:
        abstract = True

# In the event we want to score them differently by type
#Interest, etc.
class Profile(SiteInteraction):
    objects = models.Manager() #Necessary to perform queries
    #field_text = models.CharField(max_length=1000)

class Location(SiteInteraction):
    objects = models.Manager() #Necessary to perform queries

#A post, a message, etc.
class Action(SiteInteraction):
    objects = models.Manager() #Necessary to perform queries
    #field_id = models.CharField(max_length=50)
    #field_text = models.CharField(max_length=1000)


