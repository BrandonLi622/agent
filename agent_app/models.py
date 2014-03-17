from django.db import models

# TODO: - type of LI, FB ids
# "keywords" for places, etc?

# Django creates default primary keys:
# https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields

###############################################################################
# Accounts
###############################################################################

class Account(models.Model):
	def __unicode__(self):
		return self.site_name

class FacebookAccount(models.Model):
	account_id = models.ForeignKey(Account, primary_key=True)

	facebook_id = models.CharField(max_length=70) #The ID that facebook defines
	facebook_name = models.CharField(max_length=70)

	def __unicode__(self):
		return self.facebook_name

class FBFriendship(models.Model):
	facebook_id1 = models.ForeignKey(FacebookAccount)
	facebook_id2 = models.ForeignKey(FacebookAccount)

	def __unicode__(self):
		return (self.facebook_id1 + self.facebook_id2)

class LinkedInAccount(models.Model):
	account_id = models.ForeignKey(Account, primary_key=True)

	linkedin_id = models.CharField(max_length=70) #The ID that linkedin defines
	linkedin_name = models.CharField(max_length=70)

	def __unicode__(self):
		return self.linkedin_name

class LIFriendship(models.Model):
	linkedin_id1 = models.ForeignKey(LinkedInAccount)
	linkedin_id2 = models.ForeignKey(LinkedInAccount)

	def __unicode__(self):
		return (self.linkedin_id1 + self.linkedin_id2)

###############################################################################
# User
###############################################################################

class User(models.Model):
    name = models.CharField(max_length=70)
    birth_date = models.DateField()
    facebook_accountid = models.ForeignKey(FacebookAccount)
    linkedin_accountid = models.ForeignKey(LinkedInAccount)

    def __unicode__(self):
    	return self.name

###############################################################################
# Data
###############################################################################

class Place(models.Model):
	name = models.CharField(max_length=70)

	country = models.CharField(max_length=70)
	state = models.CharField(max_length=70)
	city = models.CharField(max_length=70)
	street_address = models.TextField()

	def __unicode__(self):
		return self.name

class Visits(models.Model):
    account_id = models.ForeignKey(Account)
    place = models.ForeignKey(Place)

    def __unicode__(self):
        return (account_id + ":" + str(place)) #there's probably something better for this

class Keyword(models.Model):
	word = models.CharField(max_length=70, primary_key=True) #I guess we can make this the primary key

	def __unicode(self):
		return self.word

#TODO: check that keywords is done correctly...
class Link(models.Model):
	url = models.CharField(max_length=70, primary_key=True)
	keywords = models.ManyToManyField(Keyword) #Make this a multi-valued field!

	def __unicode__(self):
		return self.url

class Messages(models.Model):
	message_id = models.CharField(max_length=70, primary_key=True)
	text = models.TextField() #How long can messages be?

	def __unicode__(self):
		return self.message_id

class Posts(models.Model):
	account_id = models.ForeignKey(Account)
	message_id = models.ForeignKey(Messages)

	def __unicode__(self):
		return (self.account_id + self.message_id)

# If a message contains multiple links, its message id shows up multiple times
class Contains(models.Model):
	message_id = models.ForeignKey(Messages)
	url = models.ForeignKey(Link)

	def __unicode__(self):
		return (self.message_id + self.url)

#Using the default primary key
class Interests(models.Model):
	name = models.CharField(max_length=70)
	type = models.CharField(max_length=70)

	def __unicode__(self):
		return self.name

class HasInterest(models.Model):
	account_id = models.ForeignKey(Account)
	interest_id = models.ForeignKey(Interests)

	def __unicode__(self):
		return (self.account_id + str(self.interest_id))
