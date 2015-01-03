import json
import urllib

from nltk.tag import pos_tag

API_KEY = open('.api-key', mode='r').read()


def get_summary(query):
    result_list = []
    keywords = extract_keywords(query)
    for keyword in keywords:
        result = freebase_search(keyword)
        topic_id = result['mid']
        summary = freebase_topic_search(topic_id)
        result_list.append(summary)
    return result_list


def extract_keywords(sentence):
    tagged = pos_tag(sentence.split())
    nouns = [word for word, pos in tagged if pos == 'NN']
    return nouns


def freebase_search(query):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'key': API_KEY
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    result = response['result'][0]
    return result


def freebase_topic_search(topic_id):
    service_url = 'https://www.googleapis.com/freebase/v1/topic'

    text_params = {
        'key': API_KEY,
        'filter': '/common/topic/article',
        'limit': 1
    }
    img_params = {
        'key': API_KEY,
        'filter': '/common/topic/image',
        'limit': 1
    }

    text_url = service_url + topic_id + '?' + urllib.urlencode(text_params)
    topic = json.loads(urllib.urlopen(text_url).read())

    # print json.dumps(topic, sort_keys=True, indent=4)

    text = topic['property']['/common/topic/article']['values'][0][
        'property']['/common/document/text']['values'][0]['value']

    img_url = service_url + topic_id + '?' + urllib.urlencode(img_params)
    topic = json.loads(urllib.urlopen(img_url).read())

    # print json.dumps(topic, sort_keys=True, indent=4)

    imgid = topic['property']['/common/topic/image']['values'][0]['id']

    return (text, imgid)
