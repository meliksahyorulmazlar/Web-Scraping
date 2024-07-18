#Resalet newspaper web scraper
#Resalet is a newspaper in Iran


import requests,os,lxml
from bs4 import BeautifulSoup

class Resalet:
    def __init__(self):
        self.first = 10580
        self.latest = self.find_latest()


    #This will find the number of the latest newspaper of Resaler
    def find_latest(self)->int:
        soup = BeautifulSoup(requests.get(url="http://paper.resalat-news.com").text,"lxml")
        for link in soup.find_all("a",href=True):
            if "nid" in link["href"]:
                number = int(link["href"].split("=")[1].strip("&pid"))
                return number

    #This method will download a nth numbered Resalet
    def download(self,number:int):
        number = str(number)
        i = str(number)
        website = f"http://paper.resalat-news.com/?nid={i}&pid=1&type=0"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        pagelinks = sorted(list(set([f'http://paper.resalat-news.com{link["href"]}' for link in soup.find_all("a", href=True) if number in link['href']])))
        os.makedirs(number)
        for i in range(len(pagelinks)):
                soup = BeautifulSoup(requests.get(url=pagelinks[i]).text,"lxml")
                download_link = soup.find("a",class_='my-3 text-dark download-specific-page')

                response = requests.get(url=f'http://paper.resalat-news.com{download_link["href"]}')
                if response.status_code == 200:
                    with open(f"{number}/{i+1}.pdf", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{number}/{i+1}.pdf was downloaded\n")
                    print(f"{number}/{i+1}.pdf was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}")

    #This method will download the entire archive of Resalet
    def download_all(self):
        for i in range(self.first,self.latest+1):
            self.download(i)

    #This will download the latest paper of Resalet
    def download_latest(self):
        self.download(self.latest)

    #This will download all the newspapers from n1 to n2
    #download_n1_n2(10600,10605)
    #It will download:
    #10600 10601 10602 10603 10604 10605 numbered Resalet newspapers
    def download_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c

        for i in range(n1,n2+1):
            self.download(i)

if __name__ == "__main__":
    resalet = Resalet()
    resalet.download_n1_n2(10600,10605)