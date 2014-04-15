from django.db import models

# TODO:
# - Required fields
# - Check field lengths

# Django creates default primary keys:
# https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields


class TermFrequency(models.Model):
    objects = models.Manager() #Necessary to perform queries
    
    freebase_mid = models.CharField(max_length=20)
    freq_count = models.IntegerField(default=0)
    
    def __unicode__(self):
	return self.freebase_mid


class User(models.Model):
    objects = models.Manager() #Necessary to perform queries

    facebook_id = models.CharField(primary_key=True, max_length=70)
    facebook_name = models.CharField(max_length=20)
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

    def __unicode__(self):
	return self.freebase_id

    # See: https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes
    class Meta:
        abstract = True

# In the event we want to score them differently by type
class Profile(SiteInteraction):
    objects = models.Manager() #Necessary to perform queries
    pass

class Location(SiteInteraction):
    pass

class Action(SiteInteraction):
    pass


