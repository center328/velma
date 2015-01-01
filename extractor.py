import json
import urllib

from nltk.tag import pos_tag

sentence = raw_input("Enter sentence:")
tagged = pos_tag(sentence.split())

propernouns = [word for word, pos in tagged if pos == 'NNP']

print tagged
print propernouns

api_key = open('.api-key', mode='r').read()
query = propernouns[0]
service_url = 'https://www.googleapis.com/freebase/v1/search'
params = {
    'query': query,
    'key': api_key
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
result = response['result'][0]
print result

service_url = 'https://www.googleapis.com/freebase/v1/topic'
topic_id = result['mid']
text_params = {
    'key': api_key,
    'filter': '/common/topic/article',
    'limit': 1
}
img_params = {
    'key': api_key,
    'filter': '/common/topic/image',
    'limit': 1
}

text_url = service_url + topic_id + '?' + urllib.urlencode(text_params)
topic = json.loads(urllib.urlopen(text_url).read())

print json.dumps(topic, sort_keys=True, indent=4)


print topic['property']['/common/topic/article']['values'][0]['property']['/common/document/text']['values'][0]['value']

img_url = service_url + topic_id + '?' + urllib.urlencode(img_params)
topic = json.loads(urllib.urlopen(img_url).read())

print json.dumps(topic, sort_keys=True, indent=4)

print topic['property']['/common/topic/image']['values'][0]['id']
