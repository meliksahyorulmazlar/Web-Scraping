#Авиация и космонавтика archive
import os
import requests,lxml
from bs4 import BeautifulSoup

class AviatsiyaKosmonavtika:
    def __init__(self):
        self.site = 'https://www.booksite.ru/avia/index.htm'
        self.year_dictionary = {}
        self.gather_years()

    # The following method will gather all the years on the
    def gather_years(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        years = [year['href'].replace(".htm","") for year in soup.find_all('a',href=True) if len(year['href']) == 8]
        for year in years:
            self.year_dictionary[int(year)] = f"https://www.booksite.ru/avia/{year}.htm"

    # The following method will download a year
    def download_year(self,year:int):
        if year in self.year_dictionary:
            os.mkdir(str(year))
            site = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                site = f"https://www.booksite.ru/avia/{pdf}"

                response = requests.get(url=site)
                if response.status_code == 200:
                    with open(f"{year}/{filename}","wb") as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f'{year}/{filename} was downloaded.\n')
                    print(f'{year}/{filename} was downloaded.')
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f'{year}/{filename} was not downloaded, it had response status code {response.status_code}\n')
                    print(f'{year}/{filename} was not downloaded, it had response status code {response.status_code}.')


    #The following method downloaded the entire archive
    def download_all(self):
        for year in self.year_dictionary:
            self.download_year(year)

    # The following method will check if a particular year downloaded it or not
    def check_year(self,year:int):
        if year in self.year_dictionary:
            try:
                os.mkdir(str(year))
            except FileExistsError:
                pass
            site = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                site = f"https://www.booksite.ru/avia/{pdf}"

                if filename not in os.listdir(f"{year}"):
                    response = requests.get(url=site)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}", "wb") as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f'{year}/{filename} was downloaded.\n')
                        print(f'{year}/{filename} was downloaded.')
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(
                                f'{year}/{filename} was not downloaded, it had response status code {response.status_code}\n')
                        print(f'{year}/{filename} was not downloaded, it had response status code {response.status_code}.')

    # The following method will check the entire archive
    def check_all(self):
        for year in self.year_dictionary:
            self.check_year(year)


if __name__ == "__main__":
    ak = AviatsiyaKosmonavtika()
    ak.check_year(1970)