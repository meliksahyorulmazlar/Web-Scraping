# Contexto Digital
import requests,os,lxml
from bs4 import BeautifulSoup


class ContextoDigital:
    def __init__(self):
        self.page = 'https://contextodedurango.com.mx/hemeroteca/'
        self.years = {}
        self.gather_files()

    # The following method will gather all the pdfs
    def gather_files(self):
        soup = BeautifulSoup(requests.get(url=self.page).text,'lxml')
        pdfs = [link['href'] for link in soup.find_all('a',href=True) if '.pdf' in link['href']]
        for pdf in pdfs:
            list_form = pdf.split("/")
            year = list_form[-3]
            if year not in self.years:
                self.years[year] = [pdf]
            else:
                self.years[year].append(pdf)

    # The following method will print all the years on the archive
    def print_years(self):
        for y in self.years:
            print(y)

    # The following method will download a specific year
    def download_year(self,year):
        if str(year) in self.years:
            pdfs = self.years[str(year)]
            if pdfs:
                os.mkdir(str(year))
                for pdf in pdfs:
                    list_form = pdf.split('/')
                    part1 = list_form[-1].replace(".pdf",'')
                    month = list_form[-2]
                    year = list_form[-3]
                    filename = f"{part1}-{month}-{year}.pdf"

                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f'{year}/{filename}','wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will download all the years
    def download_years(self):
        for y in self.years:
            self.download_year(y)

    # The following method will check if all the pdfs for a specific year has been downloaded or not
    def check_year(self,year):
        if str(year) in self.years:
            pdfs = self.years[str(year)]
            if pdfs:
                try:
                    os.mkdir(str(year))
                except FileExistsError:
                    pass
                for pdf in pdfs:
                    list_form = pdf.split('/')
                    part1 = list_form[-1].replace(".pdf",'')
                    month = list_form[-2]
                    year = list_form[-3]
                    filename = f"{part1}-{month}-{year}.pdf"

                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f'{year}/{filename}', 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")


    # The following method will check all the years
    def check_years(self):
        for y in self.years:
            self.check_year(y)

if __name__ == '__main__':
    cd = ContextoDigital()
    cd.download_year(2022)

