# Kultura

import lxml,requests,os
from bs4 import BeautifulSoup

class KulturaRossiya:
    def __init__(self):
        self.site = 'https://portal-kultura.ru/archive/year/2019/'
        self.years = {}
        self.gather_years()

    # The following method will gather all the years on the archive
    def gather_years(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        years = [link['href'] for link in soup.find_all('a',href=True) if 'year' in link['href']]
        for year in years:
            key = int(year.split("/")[-2])
            value = year
            self.years[key] = f"https://portal-kultura.ru/{value}"

    #The following method will download all the pdfs for a specific year if it is on the archive
    def download_year(self,year:int):
        if year in self.years:
            os.mkdir(f"{year}")
            soup = BeautifulSoup(requests.get(url=self.years[year]).text,'lxml')
            pdfs = [f"https://portal-kultura.ru{link['href']}" for link in soup.find_all('a',href=True) if 'pdf' in link['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                response = requests.get(url=pdf)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open(f'download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open(f'download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.\n")
                    print(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.")

    #The following method will download all the years
    def download_years(self):
        for year in self.years:
            self.download_year(year)

    # The following method will check if all the pdf for a particular year have been downloaded or not
    def check_year(self,year:int):
        if year in self.years:
            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass
            soup = BeautifulSoup(requests.get(url=self.years[year]).text, 'lxml')
            pdfs = [f"https://portal-kultura.ru{link['href']}" for link in soup.find_all('a', href=True) if 'pdf' in link['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(str(year)):
                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open(f'download_results.txt', 'a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                    else:
                        with open(f'download_results.txt', 'a') as f:
                            f.write(
                                f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.\n")
                        print(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}.")

    # The following method will check all the years to check if the pdfs have been downloaded or not
    def check_years(self):
        for year in self.years:
            self.check_year(year)


    # The following method will print all the years on the archive
    def print_years(self):
        for year in self.years:
            print(year)


if __name__ == "__main__":
    kultura = Kultura()
    kultura.download_years()
