#Y Combinator Hacker News Web Scraper
import requests,lxml
from bs4 import BeautifulSoup


class YCombinator:
    def __init__(self):
        self.hacker_soup = BeautifulSoup(requests.get(url="https://news.ycombinator.com/news").text, "lxml")
        self.articles = [span for span in self.hacker_soup.find_all("span", class_="titleline")]

        self.points = [int(span.text.strip("points").strip()) for span in self.hacker_soup.find_all("span", class_="score")]
        self.headlines = [article.find("a", href=True).text for article in self.articles]
        self.links = [article.find("a", href=True)["href"] for article in self.articles]
        #.replace("\u00a0"," ") to replace the \xa0
        self.sublines = [article.text.strip().replace("\u00a0"," ") for article in self.hacker_soup.find_all("span",class_="subline")]

    #This will show all the top 30 current headlines on the Website
    def show_all(self):
        for i in range(len(self.headlines)):
            headline = self.headlines[i]
            link = self.links[i]
            points = self.points[i]
            print(f"{i+1}. {headline}")
            print(link)
            print(self.sublines[i])

    #This will show the news with the most points
    def most_points(self):
        greatest = max(self.points)
        index = self.points.index(greatest)
        print(f"{self.headlines[index]}")
        print(self.links[index])
        print(self.sublines[index])

    #This will show the top headline
    def show_first(self):
        print(f"{self.headlines[0]}")
        print(self.links[0])
        print(self.sublines[0])



if __name__ == "__main__":
    yc = YCombinator()
    yc.show_all()
