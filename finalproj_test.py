import unittest
# from finalproj import *
from finalproj_interact import *
import sqlite3


#testing sources
# class TestSources(unittest.TestCase):
#     def test_scraping(self):
#         list_of_movies = get_movie_data()
#         self.assertEqual(len(list_of_movies), 250)
#
#     def test_more_scraping(self):
#         info = get_more_movie_data()
#         self.assertEqual(len(info), 250)
#
#     def test_get_move(self):
#         data = get_movie_data()
#         self.assertTrue(data[1], "The Godfather")
#
#     def test_get_more_data(self):
#         data = get_more_movie_data()
#         self.assertTrue(data[102], "Drama")



#test database info
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

    def test_more_column_type(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement2 = 'SELECT Title FROM Movies'
        results2 = cur.execute(statement2)
        results_list2 = results2.fetchone()
        self.assertEqual(type(results_list2), tuple)

#tests storage of the data
class TestStorage(unittest.TestCase):
    def test_data_storage(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT * FROM Movies'
        cur.execute(statement)
        results = cur.fetchall()
        self.assertEqual(len(results[0]), 4)

    def test_data_storage2(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT * FROM Movie_Info'
        cur.execute(statement)
        results = cur.fetchall()
        self.assertEqual(len(results[0]), 6)

    def test_data_storage3(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        statement = 'SELECT Director FROM Movie_Info'
        cur.execute(statement)
        results = cur.fetchall()
        self.assertNotEqual(results[0], "(USA)")


class TestInteractive(unittest.TestCase):
    def test_data(self):
        help = load_help_text()
        data = help[0]
        self.assertTrue(data, 'country')

    def test_data2(self):
        help = load_help_text()
        data = help[0]
        self.assertTrue(data, 'genre')




unittest.main()
