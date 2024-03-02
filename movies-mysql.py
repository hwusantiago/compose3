from flask import Flask
import random
import requests
from bs4 import BeautifulSoup
import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
    # crawl IMDB Top 250 and randomly select a movies
    URL = 'http://www.imdb.com/chart/top'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Error: Received HTTP status code {response.status_code}")
        exit()
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    movietags = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    movies = []
    for movie_item in movietags:
        placeAndTitle = movie_item.find('h3', class_='ipc-title__text').text.strip().split('. ')
        place = placeAndTitle[0]
        title = placeAndTitle[1]
        year = movie_item.find('span', class_='cli-title-metadata-item').text.strip()
        rating = movie_item.find('span', class_='ipc-rating-star--voteCount').previous_sibling.strip()
        movie_info = {
            'Place': place,
            'Title': title,
            'Year': year,
            'Rating': rating
        }
        movies.append(movie_info)
        # print(f'Place: #{place}, Title: {title}, Year: {year}, Rating: {rating}')
    n_movies = len(movies)
    while(True):
        idx = random.randrange(0, n_movies)
        movie = movies[idx]
        return f'Place: #{movie["Place"]}, Title: {movie["Title"]}, Year: {movie["Year"]}, Rating: {movie["Rating"]}'
        # comment the next line out to test user input with docker run -t -i
        break
        user_input = input('Do you want another movie (y/[n])? ')
        if user_input != 'y':
            break
            
@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    #cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")
    cursor.execute("USE inventory")

    cursor.execute("CREATE TABLE IF NOT EXISTS Courses (code VARCHAR(25), name VARCHAR(255))")
   
    cursor.execute("INSERT INTO Courses VALUES ('F29IP', 'Industrial Project')")
    cursor.execute("INSERT INTO Courses VALUES ('F29AI', 'Artificial Intelligence')")
    cursor.execute("INSERT INTO Courses VALUES ('F29AS', 'Advanced Software Development')")

    cursor.execute("SELECT * FROM Courses")
    result = "<h3>Courses</h3>"
    for row in cursor.fetchall():
        #print(row)
        result += row[0]+" - "+row[1]+"<br>"
    
    cursor.close()

    #return 'init database'
    return result

if __name__ == "__main__":
    app.run(host ='0.0.0.0')