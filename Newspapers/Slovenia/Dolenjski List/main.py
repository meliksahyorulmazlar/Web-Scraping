#Dolenjski list is a regional Slovenian news magazine covering Dolenjska, South Central Slovenia.
import os

import requests,lxml
from bs4 import BeautifulSoup


class DolenjskiList:
    def __init__(self):
        self.min_year = 1950
        self.max_year = 2000

    def download_year(self,year:int):
        website = f"https://dolenjskilist.svet24.si/si/dolenjski/arhiv/dl-arhiv/?l={year}"

        soup = BeautifulSoup(requests.get(url=website).text,"lxml")

        pdfs = [f"https://dolenjskilist.svet24.si{link['href']}" for link in soup.find_all("a",href=True) if "pdf" in link["href"]]

        pdfs = pdfs[1:]
        for pdf in pdfs:

            response = requests.get(url=pdf)
            filename = pdf.split("/")[-1]

            if response.status_code == 200:
                with open(f"{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    def download_d1_d2(self,year1:int,year2:int):
        if year1 > year2:
            c = year1
            year1 = year2
            year2 = c

        for i in range(year1,year2+1):
            self.download_year(i)

    def download_all(self):
        self.download_d1_d2(year1=self.min_year,year2=self.max_year)

    # The following method will check if all the newspapers for a particular newspaper have been downloaded or not
    def check_year(self,year:int):
        website = f"https://dolenjskilist.svet24.si/si/dolenjski/arhiv/dl-arhiv/?l={year}"

        soup = BeautifulSoup(requests.get(url=website).text, "lxml")

        pdfs = [f"https://dolenjskilist.svet24.si{link['href']}" for link in soup.find_all("a", href=True) if
                "pdf" in link["href"]]

        pdfs = pdfs[1:]
        for pdf in pdfs:
            filename = pdf.split("/")[-1]
            if filename not in os.listdir():
                response = requests.get(url=pdf)
                if response.status_code == 200:
                    with open(f"{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    #The following method will check all the years
    def check_years(self):
        for year in range(self.min_year,self.max_year+1):
            self.check_year(year)

if __name__ == "__main__":
    dl = DolenjskiList()
    dl.download_d1_d2(1951,dl.max_year)
