# from finalproj.py import *
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3



def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_search():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    help_text = load_help_text()
    primary_commands = ['help', 'genre', 'director', 'year', 'country']
    print("Please enter a command. Enter 'help' for assistance.")
    response = ' '
    response = input('Enter a command: ')

    while response != 'exit':
        if response.lower() == 'help':
            print(help_text)
            response = input('Enter a command: ')
            continue
        elif response.lower() == 'genre':
            statement = '''SELECT Genre, COUNT(*) FROM Movie_Info
                GROUP BY Genre
                ORDER BY COUNT(*)
            '''
            data_imdb = cur.execute(statement).fetchall()

            labels = [z[0].split()[0] for z in data_imdb]
            values = [z[1] for z in data_imdb]
            colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

            trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value',
                   textfont=dict(size=20),
                   marker=dict(colors=colors,
                               line=dict(color='#000000', width=2)))

            data = [trace]
            layout = go.Layout(
                title='Genres of Top 250 Movies',
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
            response = input("Enter a command: ")
            continue


        elif response.lower() == 'director':
            statement = ''' SELECT Director, COUNT(*) FROM Movie_Info
                GROUP BY Director
                ORDER BY COUNT(*) '''
            data_imdb = cur.execute(statement).fetchall()
            response = input("Enter a command: ")

            trace0 = go.Bar(
            x=[z[0] for z in data_imdb],
            y=[z[1] for z in data_imdb],
            marker=dict(
                color='rgb(5,0,200)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=2,
                )
            ),
            opacity=0.6
            )

            data = [trace0]
            layout = go.Layout(
                title='Directors Grouped by the Number of Movies They Directed',
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')
            response = input("Enter a command: ")
            continue

        elif response.lower() == 'country':
            statement = ''' SELECT Country, COUNT(*) FROM Movie_Info
                GROUP BY Country
                ORDER BY COUNT(*)'''
            data_imdb = cur.execute(statement).fetchall()

            labels = [z[0] for z in data_imdb]
            values = [z[1] for z in data_imdb]
            colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

            trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=20),
               marker=dict(colors=colors,
                           line=dict(color='#000000', width=2)))

            data = [trace]
            layout = go.Layout(title = 'Countries Where Top 250 Movies Were Made')
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filname='text-hover-bar')
            response = input("Enter a command: ")
            continue

        elif response.lower() == 'year':
            statement = ''' SELECT Year, COUNT(*) FROM Movies
                GROUP BY Year
                ORDER BY COUNT(*)'''
            data_imdb = cur.execute(statement).fetchall()


            trace0 = go.Bar(
            x=[z[0] for z in data_imdb],
            y=[z[1] for z in data_imdb],
            text=[z[0] for z in data_imdb],
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5,
                )
            ),
            opacity=0.6
        )

        data = [trace0]
        layout = go.Layout(
            title='Years the Top 250 Movies Were Made',
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='text-hover-bar')
        response = input("Enter a command: ")
        continue


if __name__ == '__main__':
    interactive_search()
