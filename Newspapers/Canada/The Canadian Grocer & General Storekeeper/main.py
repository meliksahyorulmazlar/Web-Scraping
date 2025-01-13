# The Canadian Grocer & General Storekeeper Archive
import os

import requests,lxml
from bs4 import BeautifulSoup

class CanadianGrocerGeneralStorekeeper:
    def __init__(self):
        self.main_page = "https://www.canadiana.ca/view/oocihm.8_06959"
        self.links = self.get_links()


    def get_links(self)->list:
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        links = [(link['href'],link.text) for link in soup.find_all("a",class_="stretched-link")]
        return links

    def print_links(self):
        print(self.links)

    # The following method will download a particular index
    def download_index(self,index:int):
        if index < len(self.links):
            paper_tuple= self.links[index]
            link = paper_tuple[0]
            filename = paper_tuple[1]

            pdf_soup = BeautifulSoup(requests.get(url=link).text,'lxml')
            link = pdf_soup.find("a",id='pvDownloadFull')
            link = link['href']

            response = requests.get(url=link)

            if response.status_code == 200:
                with open(f"{filename}.pdf","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    #The following method will download from one index to another index
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download_index(i)

    #The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(0,len(self.links))

    # The following method will check a particular index
    def check_index(self,index:int):
        if index < len(self.links):
            paper_tuple= self.links[index]
            link = paper_tuple[0]
            filename = paper_tuple[1]

            pdf_soup = BeautifulSoup(requests.get(url=link).text,'lxml')
            link = pdf_soup.find("a",id='pvDownloadFull')
            link = link['href']

            if f'{filename}.pdf' not in os.listdir():
                response = requests.get(url=link)
                if response.status_code == 200:
                    with open(f"{filename}.pdf","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will check from one index to another larger index
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.check_index(i)

    # The following method will check all the indices
    def check_all(self):
        self.check_n1_n2(0,len(self.links))

if __name__ == "__main__":
    cggs = CanadianGrocerGeneralStorekeeper()
    cggs.download_all()
