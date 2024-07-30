# Python.org events webscraper

import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Python:
    def __init__(self):
        self.start_driver()
        self.event_dictionary = {}
        self.find_events()
        print(self.event_dictionary)


    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)
        self.chrome_driver = webdriver.Chrome(options=chrome_options)
        self.chrome_driver.get(url="https://www.python.org")

    def find_events(self):
        # This set of code will find all the dates on the website
        dates = self.chrome_driver.find_elements(By.CSS_SELECTOR,".menu li time")
        dates = [date.text for date in dates]

        # The first 5 dates are for the news
        news_dates = dates[:5]
        # The last 5 dates are for the events
        event_dates = dates[5:]
        html = self.chrome_driver.page_source
        soup = BeautifulSoup(html,"lxml")

        #This will get the name of the events and their links
        old = ['Events', 'Python Events', 'User Group Events', 'Python Events Archive', 'User Group Events Archive', 'More',]
        links = [(link.text,f'https://www.python.org{link["href"]}' )for link in soup.find_all("a",href=True) if "/events/" in link["href"] and link.text not in old]

        for i in range(len(event_dates)):
            self.event_dictionary[i] = {
                "Time": event_dates[i],
                "Event": links[i][0],
                "Event Link": links[i][1]
            }

if __name__ == "__main__":
    python = Python()
