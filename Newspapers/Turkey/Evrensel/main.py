#Evrensel front page webscraper
#Evrensel is a newspaper in Turkey


import requests,lxml
from bs4 import BeautifulSoup
from selenium import webdriver


class Evrensel:
    def __init__(self):
        self.init_driver()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        self.first = 1
        self.last = self.get_last()

    #This method will initiate the selenium webdriver
    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)
        self.google_driver = webdriver.Chrome(options=chrome_options)


    #This method will find the number of the lastest copy of Evrensel
    def get_last(self)->int:
        website = "https://www.evrensel.net/fotograf/5/birinci-sayfa"
        self.google_driver.get(website)
        soup = BeautifulSoup(self.google_driver.page_source,"lxml")
        numbers = [link.text for link in soup.find_all("a",href=True) if "https://www.evrensel.net/fotograf/5/birinci-sayfa/s/" in link["href"]]
        numbers = [int(n) for n in numbers if len(n)>0]
        greatest = max(numbers)
        return greatest

    #This method will download a number
    def download(self,number:int):
        website = f"https://www.evrensel.net/fotograf/5/birinci-sayfa/s/{number}"
        self.google_driver.get(url=website)
        soup = BeautifulSoup(self.google_driver.page_source, "lxml")
        for image in soup.find_all("img", src=True, alt=True):
            if "https://www.evrensel.net/upload/fotograf/" in image["src"] or "https://www.evrensel.net/files/gallery/big/" in image["src"]:
                source = image['src']

                response = requests.get(url=source,headers=self.headers)

                if response.status_code == 200:
                    with open(f"{number}.jpg",'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{number} was downloaded\n")
                    print(f"{number} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{number} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{number} was not downloaded,it had response status code {response.status_code}")

    #This method will download all the numbers from n1 till n2
    #download_n1_n2(1,5) will download the following numbers:
    #1,2,3,4,5
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n2
            n2 = n1
            n1 = c

        for i in range(n1,n2+1):
            self.download(i)

    #This method will download all the Evrensel archive
    def download_all(self):
        self.download_n1_n2(self.first,n2=self.last)


if __name__ == "__main__":
    evrensel = Evrensel()
    evrensel.download_n1_n2(3289,evrensel.last)
