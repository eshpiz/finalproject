# finalproject

For my final project in SI 206 I used IMDB's list of "Top 250 Movies List".

Data Sources:  
The IMDB website did not require me to use an API's, so no API keys or client secrets were needed.  
I crawled and scraped through the various sites for each respective movie in the "top" list. By scraping and crawling into the various sites I was able to access the year, genre, director, length, description, etc.

Class:
I created a TopMovies class that organized the movies from the list of top movies. Each instance of the class has variables for the year it was created, the genre, director, country, and length of the film.

Key Functions:
The "get_movie_data()" function allows me to use BeautifulSoup and caching to obtain the data from the IMDB website. The caching part stores the data as a json file so that it can be accessed quickly when running other functions.
The "create_table()" function creates a data base with two tables in sqlite. I later add the data obtained from the scraping and crawling and import it into the database. The two tables are connected through a foreign/primary key that links the movie information between the two tables.

Interactive:
I use another file called "finalproj_interactive.py" to give the user prompts and use that information to present various data. The user is prompted with a command line and can choose help, which will give them a list of possible commands and what the commands do. Other commands include country which will present a pie chart of where the various movies were created. The genre command will generate a pie chart of the various genres. The director command will create a a bar chart of the directors who created the various movies. Lastly, the year command generates a bar graph of the years the movies were created.

Files:
The finalproj.py file gets the table from the websites and then scrapes/crawls through the sites. This file also creates the DB table and then puts the information into the tables. The finalproj_interact gives the user prompts and creates the plotly graphs. 
