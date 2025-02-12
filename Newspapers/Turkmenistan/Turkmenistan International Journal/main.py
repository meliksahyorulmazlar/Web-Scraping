# Turkmenistan International Journal

import requests,os,lxml
from bs4 import BeautifulSoup

class TurkmenistanInternationalJournal:
    def __init__(self):
        self.year_dictionary = {}
        self.gather_years()


    # The following method will gather all the years on the archive
    def gather_years(self):
        website = 'https://www.turkmenistaninfo.ru/?page_id=6&lang_id=en&&sort=date_desc'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [(page.text,f"https://www.turkmenistaninfo.ru/{page['href']}") for page in soup.find_all('a',href=True) if len(page.text) == 4]
        for page in pages:
            key = page[0]
            value = page[1]
            self.year_dictionary[key] = value

    # The following method will print all the years on the archive
    def print_years(self):
        for year in self.year_dictionary:
            print(year)

    # The following method will download a specific year on the archive
    def download_year(self,year:str):
        if year in self.year_dictionary:
            os.mkdir(year)
            website = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            magazines = [f"https://www.turkmenistaninfo.ru/{mag['href']}" for mag in soup.find_all('a',href=True,class_='magazine_title')]
            for mag in magazines:
                soup = BeautifulSoup(requests.get(mag).text,'lxml')
                pdf = soup.find('a',href=True,class_='pdf_version')
                pdf_link = "https://www.turkmenistaninfo.ru/"+ pdf['href']
                filename = pdf_link.split("/")[-1]
                response = requests.get(pdf_link)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{year}/{filename} was downloaded, it had response status code {response.status_code}")

    # The following method will download all the years on the archive
    def download_all(self):
        for year in self.year_dictionary:
            self.download_year(year)

    # The following method will check a particular year
    def check_year(self,year:str):
        if year in self.year_dictionary:
            try:
                os.mkdir(year)
            except FileExistsError:
                pass
            website = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            magazines = [f"https://www.turkmenistaninfo.ru/{mag['href']}" for mag in soup.find_all('a',href=True,class_='magazine_title')]
            for mag in magazines:
                soup = BeautifulSoup(requests.get(mag).text,'lxml')
                pdf = soup.find('a',href=True,class_='pdf_version')
                pdf_link = "https://www.turkmenistaninfo.ru/"+ pdf['href']
                filename = pdf_link.split("/")[-1]
                if filename not in os.listdir(f"{year}"):
                    response = requests.get(pdf_link)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{year}/{filename} was downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{year}/{filename} was already downloaded.")

    # The following method will check the entire archive
    def check_all(self):
        for year in self.year_dictionary:
            self.check_year(year)

if __name__ == "__main__":
    tij = TurkmenistanInternationalJournal()
    tij.check_all()