from django.db import models

# TODO: - type of LI, FB ids
# "keywords" for places, etc?

# Django creates default primary keys:
# https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields

###############################################################################
# Accounts
###############################################################################

#Django creates default primary keys:
#https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields

class User(models.Model):
    facebook_name = models.CharField(max_length=20)
    facebook_id = models.CharField(max_length=70) # TODO: check length
    last_updated = models.DateField()

    def __unicode__(self):
		return self.facebook_name

class SiteInteraction(models.Model):
    user_id = models.ForeignKey(User)

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
    pass

class Location(SiteInteraction):
    pass

class Action(SiteInteraction):
    pass
