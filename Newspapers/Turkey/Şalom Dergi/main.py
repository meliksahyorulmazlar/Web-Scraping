#Şalom(shalom which means hello in Hebrew) Dergi pdf downloader
#A Jewish magazine published in Turkey
import os

from bs4 import BeautifulSoup
import requests,lxml,datetime

class SalomDergi:
    def __init__(self):
        #The lowest/oldest number magazine on the website
        self.lowest = 5
        self.main_soup = BeautifulSoup(requests.get(url="https://dergi.salom.com.tr/tum-dergiler").text,"lxml")
        #This is the lastest number of the magazine
        self.latest = None
        #The numbers/titles missing from the website
        self.missing = [1,2,3,4,5,11,30,32,45,82,83,84,85,86,87,88,89]
        self.find_latest()

    #This will find the number/title of the latest magazine of Şalom Dergi
    def find_latest(self):
        self.pdf = [link["href"] for link in self.main_soup.find_all("a",href=True,title=True) if "dergi-" in link["href"]][0]
        self.latest = int(self.pdf.split("-")[1])

    # The following method will download the number
    def download(self,number:int):
        website = f"https://dergi.salom.com.tr/dergi-{number}-1_1"
        page_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        for link in page_soup.find_all("a", href=True):
            if link.text == "Dergiyi okumak için tıklayın":
                download_link = link["href"]

                response = requests.get(url=download_link)
                pdf_name = download_link.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{pdf_name}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{pdf_name} was downloaded")
                    print(f"{pdf_name} was downloaded")
                else:
                    print(f"{pdf_name} was not downloaded,it had response status code")
                    with open("download_results.txt", "a") as f:
                        f.write(f"{pdf_name} was not downloaded,it had response status code")

    #This will download all of the magazines found on the website
    def download_all(self):
        for i in range(self.lowest, self.latest + 1):
            if i not in self.missing:
                self.download(number=i)


    #This will download a number if it is on the website
    def download_number(self,number:int):
        if number in self.missing:
            print(f"{number} is missing from the website therefore it cannot be downloaded")
        elif number>self.latest:
            print(f"That number does not exist,therefore it cannot be downloaded")
        else:
            self.download(number=number)

    # The following method will check a particular number to check if it has been downloaded or nor
    def check_number(self,number:int):
        if number in self.missing:
            print(f"{number} is missing from the website therefore it cannot be downloaded")
        elif number>self.latest:
            print(f"That number does not exist,therefore it cannot be downloaded")
        else:
            self.check(number=number)

    # The following method will check
    def check(self,number:int):
        website = f"https://dergi.salom.com.tr/dergi-{number}-1_1"
        page_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        for link in page_soup.find_all("a", href=True):
            if link.text == "Dergiyi okumak için tıklayın":
                download_link = link["href"]


                pdf_name = download_link.split("/")[-1]
                if pdf_name not in os.listdir():
                    response = requests.get(url=download_link)
                    if response.status_code == 200:
                        with open(f"{pdf_name}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{pdf_name} was downloaded")
                        print(f"{pdf_name} was downloaded")
                    else:
                        print(f"{pdf_name} was not downloaded,it had response status code")
                        with open("download_results.txt", "a") as f:
                            f.write(f"{pdf_name} was not downloaded,it had response status code")

    # The following method will check from one number to another later number
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.check(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(self.lowest,self.latest)

if __name__ == "__main__":
    sd = SalomDergi()
    sd.download_all()
