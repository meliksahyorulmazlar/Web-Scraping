#Olonetskiye Gubernskiye Vedomosti archive

import requests,os,lxml
from bs4 import BeautifulSoup

class OlonetskiyeGubernskiyeVedomosti:
    def __init__(self):
        self.site = 'https://ogv.karelia.ru/catalog.shtml'
        self.years = {}
        self.gather_years()

    # The following method will gather all the years on the archive
    def gather_years(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        years = [f"https://ogv.karelia.ru/catalog.shtml{year['href']}" for year in soup.find_all('a',href=True) if 'year' in year['href']]

        for year in years:
            key = int(year.split("=")[-1])
            value = year
            self.years[key] = value
        print(self.years)

    # The following method will download a specific year if it is on the archive
    def download_year(self,year:int):
        if year in self.years:
            os.mkdir(f"{year}")
            soup = BeautifulSoup(requests.get(url=self.years[year]).text,'lxml')
            papers = [f"https://ogv.karelia.ru/{paper['href']}" for paper in soup.find_all('a',href=True) if 'id' in paper['href']]
            #The first two are irrelevant
            papers = papers[2:]
            for paper in papers:
                print(paper)
                new_soup = BeautifulSoup(requests.get(url=paper).text,'lxml')
                pdf = [f"https://ogv.karelia.ru{link['href']}" for link in new_soup.find_all('a',href=True) if 'pdf' in link['href']]
                pdf = pdf[0].replace("..","")
                filename = pdf.split("/")[-1]
                response = requests.get(url=pdf)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.\n")
                    print(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.")


    # The following method will download all the years on the archive
    def download_years(self):
        for year in self.years:
            self.download_year(year)

    # The following method will check if all the pdfs for a specific year have been downloaded or not
    def check_year(self,year:int):
        if year in self.years:
            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass
            soup = BeautifulSoup(requests.get(url=self.years[year]).text, 'lxml')
            papers = [f"https://ogv.karelia.ru/{paper['href']}"for paper in soup.find_all('a', href=True) if 'id' in paper['href']]
            # The first two are irrelevant
            papers = papers[2:]
            for paper in papers:
                new_soup = BeautifulSoup(requests.get(url=paper).text, 'lxml')
                pdf = [f"https://ogv.karelia.ru{link['href']}" for link in new_soup.find_all('a', href=True) if'pdf' in link['href']]
                pdf = pdf[0].replace("..", "")
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(f"{year}"):
                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.\n")
                        print(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.")

    # The following method will check all the years on the archive
    def check_years(self):
        for year in self.years:
            self.check_year(year)

    # The following method will print all the valid years on the archive
    def print_years(self):
        for year in self.years:
            print(year)


if __name__ == "__main__":
    ogv = OlonetskiyeGubernskiyeVedomosti()
    ogv.download_year(year=1914)
