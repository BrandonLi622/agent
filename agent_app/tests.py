"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import agent_app.freebase as fb
from agent_app.models import User, Profile

# TODO:
# - assertions

class FreebaseTest(TestCase):
    def test_search(self):
        search_results = fb.search('apple')

    def test_get_topic_mid(self):
        topic = fb.get_topic('/m/0k8z')


    def test_get_topic_id(self):
        topic = fb.get_topic('/book/publishing_company')
        self.assertEqual(topic['property']['/type/object/mid']['values'][0]['text'],
                '/m/01xryxp')

    def test_id_to_mid(self):
        mid = fb.id_to_mid('/book/publishing_company')
        self.assertEqual(mid, '/m/01xryxp')

    def test_entities_to_topics(self):
        topics = fb.entities_to_topics(['apple', 'Bob Marley'])

    def test_add_interaction(self):
        user = User(facebook_id='TEST',facebook_name='Daniel')
        user.save()
        fb.add_interaction(user, Profile, ['apple', 'Bob Marley'])
        user.delete()
'''
class RecommenderTest(TestCase):
    def null():
        pass'''
