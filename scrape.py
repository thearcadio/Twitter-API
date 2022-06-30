# script adapted from:
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/master/Full-Archive-Search/full-archive-search.py

import requests
import Secret
import json
import time

search_url = "https://api.twitter.com/2/tweets/search/all"
headers = {"Authorization": "Bearer {}".format(Secret.token)}
count = 0
pages = 0

def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    retries=0
    sleep_time = 60
    while response.status_code == 429 and retries <3:
        print(f'429. Sleeping for {sleep_time*(retries+1)} seconds and then retrying...')
        time.sleep(sleep_time*(retries+1))
        response = requests.request("GET", url, headers=headers, params=params)
        retries+=1
    if retries == 3:
        print('Maximum retries exceeded. Please try again')
    return response.json()

def init_search(query_params, next_token=None):
    query_params['next_token'] = next_token
    payload = connect_to_endpoint(search_url, headers, query_params)
    for tweet in payload['data']:
        global count
        count+=1
        yield(tweet)
    global pages
    pages+=1
    print(f'{count} tweets loaded and ' + f'{pages} total pages loaded')
    # the pages limit can be changed to cap how many tweets you pull
    # this ties directly to your query
    # max tweets = pages * max results
    # for example, 20 pages and max results of 500 will give you up to 10,000 tweets
    if 'next_token' in payload['meta'] and pages < 20: # change the number here to limit tweets pulled
        time.sleep(1)
        yield from init_search(query_params, next_token=payload['meta']['next_token'])

def search(query_params, next_token=None):
    data = init_search(query_params, next_token=next_token)
    frame = []
    for tweet in data:
        frame.append(tweet)
    return frame

def save(payload, filename):
    if filename[-4:]!='json':
        filename.append('.json')
    with open(filename,'w') as f:
        json.dump(payload, f)
