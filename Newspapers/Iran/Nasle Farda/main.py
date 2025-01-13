#Nasle Farda pdf webscraper
#Nasle Farda is a newspaper in Iran

import requests,lxml,os
from bs4 import BeautifulSoup

class NasleFarda:
    def __init__(self):
        self.first = 4809
        self.latest = self.find_latest()
        print(self.latest)

    #This method will download the number of the latest of the newspaper
    def find_latest(self)->int:
        page = "http://naslefarda.net"
        soup = BeautifulSoup(requests.get(url=page).text,"lxml")
        for link in soup.find_all("a",href=True):
            if "nid" in link["href"]:
                number = int(link["href"].split("=")[1].strip("&pnid"))
                return number

    #This method will initiate the download
    def gather_download_data(self,number:int)->list:
        number = str(number)
        link = f"http://naslefarda.net/?nid={number}&pid=1&type=0"
        soup = BeautifulSoup(requests.get(url=link).text, "lxml")
        links = [td.find("a")["href"] for td in soup.find_all('td', class_="pagelink")]
        links = [f"http://naslefarda.net{link}" for link in links]
        return links


    #This method will download the pdfs of that newspaper
    def download(self,number:str):
        if self.first <= number <= self.latest:
            links = self.gather_download_data(n)
            os.mkdir(number)
            for link in links:
                new_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
                try:
                    image_link = [f"http://naslefarda.net{anchor['href']}" for anchor in new_soup.find_all("a", href=True) if "pagepdf" in anchor["href"]][0]
                except IndexError:
                    with open("download_results.txt","a") as f:
                        f.write(f"{link} was not downloaded-index error\n")
                    continue
                filename = (image_link.split("/")[-1]) + ".pdf"
                response = requests.get(url=image_link)
                if response.status_code == 200:
                    with open(f"{number}/{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{filename} was downloaded\n")
                    print(f"{number}/{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{filename} was not downloaded,it had response statud code {response.status_code}\n")
                    print(f"{number}/{filename} was not downloaded,it had response statud code {response.status_code}")

    #This method will download all the newspapers
    def download_all(self):
        for i in range(self.first,self.latest+1):
            self.download(i)

    #This method will download all the newspapers from n1 to n2
    #download_n1_n2(5500,5505)
    #The following example will download  5500 5501 5502 5503 5504 5505 numbered newspapers
    def download_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.download(i)

    #This method will download the nth numbered newspaper
    def download_number(self,number:int):
        self.download(number)

    #This method will download the latest number of Nasle Farda
    def download_latest(self):
        self.download(number=self.latest)

    # The following method will check to see if the images have been downloaded or not
    def check(self,number:int):
        if self.first <= number <= self.latest:
            try:
                os.mkdir(number)
            except FileExistsError:
                pass
            links = self.gather_download_data(number)
            for link in links:
                new_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
                try:
                    image_link = [f"http://naslefarda.net{anchor['href']}" for anchor in new_soup.find_all("a", href=True) if "pagepdf" in anchor["href"]][0]
                except IndexError:
                    with open("download_results.txt","a") as f:
                        f.write(f"{link} was not downloaded-index error\n")
                    continue
                filename = (image_link.split("/")[-1]) + ".pdf"
                response = requests.get(url=image_link)
                if response.status_code == 200:
                    with open(f"{number}/{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{filename} was downloaded\n")
                    print(f"{number}/{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{filename} was not downloaded,it had response statud code {response.status_code}\n")
                    print(f"{number}/{filename} was not downloaded,it had response statud code {response.status_code}")

    # The following method will check from the n1th number till the n2nd number
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.check(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(self.first,self.latest)

if __name__ == "__main__":
    ne = NasleFarda()
    ne.download_all()
