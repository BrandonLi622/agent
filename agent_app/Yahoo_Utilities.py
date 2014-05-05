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

import string
import requests
import json
import logging
#logging.disable(logging.CRITICAL)


def extract_entities(search_string):
	search_string.replace('"','');
	q = 'SELECT * FROM contentanalysis.analyze WHERE text = "' + search_string +'"'
	logging.warning("what is q: " + q)
	r = requests.get('https://query.yahooapis.com/v1/public/yql?q='+q+'&format=json')
	
	js = r.json()
	results = js['query']['results']
	resultlist = []
	
	logging.warning("js from yahoo: " + str(js))
	logging.warning("search string: " + search_string)

	try:
		if results is not None:
			logging.warning("Results are not none!!")
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
		
		if len(resultlist) == 0:
			return search_string.split(' ')
	except Exception as e:
		logging.warning("Exception in Yahoo_Utilities: " + str(e))
	return resultlist