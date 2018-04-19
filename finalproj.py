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
  def __init__(self, rank, title, year, movie_url=None):
    self.rank = rank
    self.title = title
    self.year = year
    self.url = movie_url

    if movie_url == None:
      self.director = " "
      self.content_rating = " "
      self.length = " "
      self.genre = " "
      self.country = "  "

    else:
      html3 = make_request_using_cache(movie_url)
      page_soup = BeautifulSoup(html3, 'html.parser')
      data = page_soup.find('div',id="main_top")
      self.director = data.find('span', itemprop="director").text
      self.length = data.find('time', itemprop="duration").text
      temp = [link.string for link in data.find_all('span', itemprop="genre")]
      self.genre = ",".join(temp)
      bottom_info = page_soup.find(id="titleStoryLine")
      self.storyline = bottom_info.find('div', class_="inline canwrap").text
      more_data = page_soup.find(id="titleDetails")
      table_info = more_data.find_all('div', class_="txt-block")[1]
      self.country = table_info.find(itemprop="url").text


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
  return titles_list

def get_more_movie_data():
  url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'
  html = make_request_using_cache(url)
  soup2 = BeautifulSoup(html, 'html.parser')
  base_url = 'http://www.imdb.com/'

  menu = soup2.find(class_="lister-list")
  title_col = menu.find_all(class_="titleColumn")
  #print(title_col)
  url_list = []
  for x in title_col:
    movie_url = base_url + x.a['href']
    url_list.append(movie_url)
  #print(url_list)
  return(url_list)
x = get_more_movie_data()

movie_class = []
counter = 0
for movie in get_movie_data():
  movie_class += [TopMovies(movie[0], movie[1], movie[2], movie_url = x[counter])]
  counter += 1


def create_objects():
  #put info in movie class/ creates objects
  try:
    movies_dict = {}
    for title in get_movie_data():
      movies_dict[title[1]] = {'year':title[2], 'rank':title[0]}
  except:
    None


def create_table():
  conn = sqlite3.connect('movies.db')
  cur = conn.cursor()
  movies_drop = 'DROP TABLE IF EXISTS "Movies"'
  movie_info_drop = 'DROP TABLE IF EXISTS "Movies_Info"'
  cur.execute(movies_drop)
  cur.execute(movie_info_drop)

  #Create movies
  statement = ''' CREATE TABLE 'Movies' (
      'Id' INTEGER PRIMARY KEY,
      'Rank' INTEGER NOT NULL,
      'Title' TEXT NOT NULL,
      'Year' Integer
  );
  '''
  cur.execute(statement)
  conn.commit()

  statement2 = ''' CREATE TABLE 'Movie_Info' (
      'Id' INTEGER PRIMARY KEY,
      'Rank' INTEGER NOT NULL,
      'Director' TEXT,
      'Length' TEXT,
      'Genre' TEXT,
      'Country' TEXT
  );
  '''
  cur.execute(statement2)
  conn.commit()
  conn.close()

  conn = sqlite3.connect('movies.db')
  cur = conn.cursor()
  for x in movie_class:
      query = '''INSERT INTO Movies (Id, Rank, Title, Year) VALUES (?,?,?,?)
      '''
      data = (None, x.rank, x.title, x.year)
      cur.execute(query, data)
  conn.commit()
  conn.close()

  conn = sqlite3.connect('movies.db')
  cur = conn.cursor()
  for x in movie_class:
    query1 = ''' INSERT INTO Movie_Info (Id, Rank, Director, Length, Genre, Country) VALUES (?,?,?,?,?,?)
    '''
    data1 = (None, x.rank, x.director, x.length, x.genre, x.country)
    cur.execute(query1, data1)
  conn.commit()
  conn.close



def update_table():
  # Deletes white space in title column
  conn = sqlite3.connect('movies.db')
  cur = conn.cursor()
  statement = ''' UPDATE Movies
      SET Title = LTRIM(Title)'''

  statement2 = '''UPDATE Movies
    SET Length = LTRIM(RTRIM(Length))'''
  cur.execute(statement)
  cur.execute(statement2)


  update = '''UPDATE Movies
      SET Rank = (
      SELECT Rank
      FROM Movie_Info
      WHERE Movies.Rank = Movie_Info.Rank
      )
  '''
  cur.execute(update)
  conn.commit()
  conn.close()



create_table()
update_table()
