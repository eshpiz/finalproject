#Emma Shpiz Final Project

import secrets
from bs4 import BeautifulSoup
import requests
import json


#caching
#parks caching
#
# CACHE_FNAME = 'most_pop_movies.json'
# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()
# except:
#     CACHE_DICTION = {}
#
# def get_unique_key(url):
#   return url
#
# def make_request_using_cache(url):
#     unique_ident = get_unique_key(url)
#
#     if unique_ident in CACHE_DICTION:
#         print("Getting cached data...")
#         return CACHE_DICTION[unique_ident]
#
#     else:
#         print("Making a request for new data...")
#         # Make the request and cache the new data
#         resp = requests.get(url)
#         CACHE_DICTION[unique_ident] = resp.text
#         dumped_json_cache = json.dumps(CACHE_DICTION)
#         fw = open(CACHE_FNAME,"w")
#         fw.write(dumped_json_cache)
#         fw.close() # Close the open file
#         return CACHE_DICTION[unique_ident]
#



html = requests.get('http://www.imdb.com/chart/top?ref_=nv_mv_250_6').text
soup = BeautifulSoup(html, 'html.parser')

search_titles = soup.find(class_="chart full-width")
table_rows = search_titles.find_all('tr')
for tr in table_rows:
    table_titles = tr.find_all('td')
    titles_list = []
    if len(table_titles) == 5:
        titles = table_titles[1].text.strip()
        titles_list.append(titles)
        print(titles_list)
        # for i in table_titles:
        #     titles = (.text.strip())
        #     print(titles)



# titles = search_titles.find('a')

# for x in search_titles:
#     print(x.get_text())
# titles = []
# for i in search_titles:
#     titles.append({"title":i.get_text()})
# print(titles)
