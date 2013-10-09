from sdk_python.alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

def stringToSentiment(string):
	response = alchemyapi.sentiment('text', string)

	if response['status'] == 'OK':
		if response['docSentiment']['type'] != "neutral":
			return response['docSentiment']['score']
		else:
			return 0.0
	else:
		print ('Error.')

def stringToEntities(string, attribute = None):
  response = alchemyapi.entities('text', string, {'sentiment' : 1})
  if response['status'] == 'OK':
    if attribute == None:
      return response['entities']
    else:
      returnArr = []
      for entity in response['entities']:
        returnArr.append(entity[attribute])
      return returnArr
  else:
    print('Error.')

def stringToConcepts(string, attribute = None):
  response = alchemyapi.concepts('text', string)
  if response['status'] == 'OK':
    if attribute == None:
      return response['concepts']
    else:
      returnArr = []
      for concept in response['concepts']:
        returnArr.append(concept[attribute])
      return returnArr
  else:
    print('Error in concept call')

def stringToKeywords(string, attribute = None):
  response = alchemyapi.keywords('text', string, {'sentiment' : 1})
  if response['status'] == 'OK':
    if attribute == None:
      return response['keywords']
    else:
      returnArr = []
      for keyword in response['keywords']:
        returnArr.append(keyword[attribute])
  else:
    print('Error')

def stringToCategory(string):
  response = alchemyapi.category('text', string)
  if response['status'] == 'OK':
    return [response['category'], response['score']]
  else:
    print('Error')

def stringToRelation(string, attribute = None):
  response = alchemyapi.relations('text', string)
  if response['status'] == 'OK':
    if attribute == None:
      return response['relations']
    else:
      returnArr = []
      for relation in response['relations']:
        returnArr.append(relation[attribute]['text'])
      return returnArr
  else:
    print('Error')
