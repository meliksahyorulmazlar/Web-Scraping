#Webscraper to get the Empire's top 100 movies of all time
import requests
from bs4 import BeautifulSoup


class EmpireMovies:
    def __init__(self):
        self.website = "https://www.empireonline.com/movies/features/best-movies-2/"
        self.movie_soup = BeautifulSoup(requests.get(url=self.website).text,"lxml")
        self.get_titles()
        self.text = []

    #This gets the titles of all the movies
    def get_titles(self):
        self.movies = [movie.text for movie in self.movie_soup.find_all("h3")]

    #This will show all the movies ordered from first to last
    def show_titles(self):
        print(self.movies[::-1])


    #This creates a text file of the movies ordered from first to last
    def create_textfile(self):
        for movie in self.movies[::-1]:
            with open("empire_movies.txt","a") as f:
                f.write(f"{movie}\n")
    def show_movies(self):
        movies = self.movies[::-1]
        for i in range(len(self.movies)):
            print(movies[i])


if __name__ == "__main__":
    em = EmpireMovies()
    em.show_movies()
