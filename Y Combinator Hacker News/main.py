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

        #On the Y Combinator news they add job positions and this is the code to get extra subline and will assign 0 points for those articles
        extra_subtext = [td.text.strip("\n") for td in self.hacker_soup.find_all("td", class_="subtext") if "comment" not in td.text]
        extra_index = 0
        for headline in self.headlines:
            if "YC" in headline and "Hiring" in headline:
                index = self.headlines.index(headline)
                self.points.insert(index,0)
                self.sublines.insert(index,extra_subtext[extra_index])
                extra_index += 1

        # This will find how many comments there are for each article
        self.comments = []
        for subline in self.sublines:
            splits = [split.strip() for split in subline.split("|")]
            if "comments" in splits[-1]:
                last_item = int(splits[-1].strip("comments").strip())
                self.comments.append(last_item)
            elif "comment" in splits[-1]:
                last_item = int(splits[-1].strip("comment").strip())
                self.comments.append(last_item)
            else:
                self.comments.append(0)


    #This method will show all the top 30 current headlines on the Website
    def show_all(self):
        for i in range(len(self.headlines)):
            headline = self.headlines[i]
            link = self.links[i]
            points = self.points[i]
            print(f"{i+1}. {headline}")
            print(link)
            print(self.sublines[i])
        print()

    #This method will show the news with the most points
    def most_points(self):
        greatest = max(self.points)
        index = self.points.index(greatest)
        print(f"{self.headlines[index]}")
        print(self.links[index])
        print(self.sublines[index])
        print()

    # This method will show the article with the most comments
    def most_comments(self):
        greatest = max(self.comments)
        index = self.comments.index(greatest)
        print(f"{self.headlines[index]}")
        print(self.links[index])
        print(self.sublines[index])
        print()

    #This method will show the top headline
    def show_first(self):
        print(f"{self.headlines[0]}")
        print(self.links[0])
        print(self.sublines[0])
        print()




if __name__ == "__main__":
    yc = YCombinator()
    yc.show_all()
    yc.show_first()
    yc.most_points()
    yc.most_comments()
