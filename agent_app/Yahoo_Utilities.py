import string
import requests
import json
import logging


def extract_entities(search_string):
	search_string.replace('"','');
	q = 'SELECT * FROM contentanalysis.analyze WHERE text = "' + search_string +'"'
	r = requests.get('https://query.yahooapis.com/v1/public/yql?q='+q+'&format=json')
	js = r.json()
	results = js['query']['results']
	resultlist = []

	if results is not None:
		if 'entities' in results:
			entities = results['entities']['entity']
			if type(entities) is list:
				for entity in entities:
					if 'text' in entity:
						resultlist[len(resultlist):] = [entity['text']['content']]
			else:
				if 'text' in entities:
					resultlist[len(resultlist):] = [entities['text']['content']]
		if  'yctCategories' in results:
			categories = results['yctCategories']['yctCategory']
			if type(categories) is list:
				for category in categories:
					resultlist[len(resultlist):] = [category['content']]
			else:
				resultlist[len(resultlist):] = [categories['content']]
	return resultlist