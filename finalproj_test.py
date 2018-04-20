import unittest
# from finalproj import *
from finalproj_interact import *
import sqlite3


#testing sources
# class TestSources(unittest.TestCase):
#     def test_scraping(self):
#         list_of_movies = get_movie_data()
#         self.assertEqual(len(list_of_movies), 250)

#test database
class TestDatabase(unittest.TestCase):
    def test_movie_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Title FROM Movies'
        results = cur.execute(statement)
        results_list = results.fetchall()
        self.assertEqual(len(results_list), 250)

    def test_movie_info_table(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Director FROM Movie_Info'
        results = cur.execute(statement)
        results_list = results.fetchall()
        self.assertEqual(len(results_list), 250)

    def test_first_movie(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Title FROM Movies'
        results = cur.execute(statement)
        results_list = results.fetchone()
        self.assertTrue(results_list,'The Shawshank Redemption')

    def test_first_country(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Country FROM Movie_Info'
        results = cur.execute(statement)
        results_list = results.fetchone()
        self.assertTrue(results_list, '(USA)')

    def test_column_type(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Director FROM Movie_Info'
        results = cur.execute(statement)
        results_list = results.fetchone()
        self.assertEqual(type(results_list), tuple)
        statement2 = 'SELECT Title FROM Movies'
        results2 = cur.execute(statement2)
        results_list2 = results.fetchone()
        self.assertEqual(type(results_list2), tuple)





unittest.main()
