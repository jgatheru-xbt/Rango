import json
import urllib

import requests


def read_api_key():

    api_key = None

    try:
        with open('serp.key', 'r') as key_f:
            api_key = key_f.readline()

    except:
        raise  IOError ('bing.key file not found')

    return api_key


def run_query(search_items):
    """
    given a string containing search terms(query), returns a list of results from the bing search engine.
    """

    api_key = read_api_key()

    if not api_key:
        raise KeyError("Api Key Not Found")

    #specifying the base url and the service(Bing Search API 2.0)
    root_url = 'https://serpapi.com/search.json?engine=google'


    query = f"{root_url}&q={search_items}&api_key={api_key}"
    response = requests.get(query)
    json_response = response.json()

    return json_response



if __name__ == "__main__":
    run_query("python")
