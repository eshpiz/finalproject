#Emma Shpiz Final Project

from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import sys



#Caching top movies list

try:
    cache_file = open('top_movies.json', 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open('top_movies.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



class TopMovies:
  def __init__(self, rank, title, year, site_url=None):
    self.rank = rank
    self.title = title
    self.year = year
    self.url = site_url

    if site_url == None:
      self.user_rating = " "
      self.director = " "
      self.content_rating = " "
      self.length = " "
      self.genre = " "

    else:
      html3 = make_request_using_cache(site_url)
      page_soup = BeautifulSoup(html3, 'html.parser')
      data = page_soup.find('div',id="main_top")
      self.user_rating = data.find('span', itemprop="ratingValue")
      self.director = data.find('span', itemprop="director")
      self.content_rating = data.find('meta', itemprop="contentRating")
      self.length = data.find('time', itemprop="duration")
      self.genre = data.find_all('span', itemprop="genre")

  def __str__(self):
    return (self.rank + self.title + self.year)

def get_movie_data():
  url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'
  html = make_request_using_cache(url)
  soup = BeautifulSoup(html, 'html.parser')

  search_titles = soup.find(class_="chart full-width")
  table_rows = search_titles.find_all('tr')
  titles_list = []
  DELIMITER = '\n'
  for tr in table_rows:
      table_titles = tr.find_all('td')
      if len(table_titles) == 5:
          titles = table_titles[1].text.strip().split(DELIMITER)
          titles_list.append(titles)
  #print(titles_list)
  return titles_list

movie_class = []
for movie in get_movie_data():
  movie_class += [TopMovies(movie[0], movie[1], movie[2])]

movies_dict = {}
for title in get_movie_data():
  movies_dict[title[1]] = {'year':title[2], 'rank':title[0]}
#print(movies_dict)
#movies_dict.update(get_movie_data())
#print

try:
  movies_dict = {}
  for title in get_movie_data():
    movies_dict[title[1]] = {'year':title[2], 'rank':title[0]}
except:
  None
for x in movie_class:
  print(x)

#
# with f as open(r'top_movies', 'wb'):
#     f.write(str(sliced_data))
#     f.close()

conn = sqlite3.connect('movies.db')
cur = conn.cursor()
movies_drop = 'DROP TABLE IF EXISTS "Movies"'


cur.execute(movies_drop)

#Create movies
statement = ''' CREATE TABLE 'Movies' (
    'Id' INTEGER PRIMARY KEY,
    'Rank' TEXT NOT NULL,
    'Title' TEXT NOT NULL,
    'Year' TEXT
);
'''
cur.execute(statement)
conn.commit()


conn = sqlite3.connect('movies.db')
cur = conn.cursor()
for x in movie_class:
    query = '''INSERT INTO Movies (Id, Rank, Title, Year) VALUES (?,?,?,?)
    '''
    data = (None, x.rank, x.title, x.year)
    cur.execute(query, data)
conn.commit()
conn.close()
