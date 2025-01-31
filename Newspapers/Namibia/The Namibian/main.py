# The Namibian
from http.client import responses

import requests,os,lxml
from bs4 import BeautifulSoup



class TheNamibian:
    def __init__(self):
        self.years = [year for year in range(1985,1995)]

    # The following method will print all the years on the archive
    def print_years(self):
        for year in self.years:
            print(year)

    # The following method will download a specific year on the archive
    def download_year(self,year:int):
        if year in self.years:
            os.mkdir(f"{year}")
            site = f"https://old.namibian.com.na/archive_pdf_19851990/{year}_TheNamibian/"
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                pdf = pdf.replace("%20"," ")
                website = f"https://old.namibian.com.na/archive_pdf_19851990/{year}_TheNamibian/{pdf}"
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{year}/{pdf}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{pdf} was downloaded.\n")
                    print(f"{year}/{pdf} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{pdf} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{year}/{pdf} was downloaded, it had response status code {response.status_code}")

    # The following method will download all the years on the archive
    def download_years(self):
        for year in self.years:
            self.download_year(year)

    # The following method will check a specific year to see if all the pdfs have been downloaded or not
    def check_year(self,year:int):
        if year in self.years:
            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass
            site = f"https://old.namibian.com.na/archive_pdf_19851990/{year}_TheNamibian/"
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                pdf = pdf.replace("%20", " ")
                if pdf not in os.listdir(f"{year}"):
                    website = f"https://old.namibian.com.na/archive_pdf_19851990/{year}_TheNamibian/{pdf}"
                    response = requests.get(url=website)
                    if response.status_code == 200:
                        with open(f"{year}/{pdf}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{year}/{pdf} was downloaded.\n")
                        print(f"{year}/{pdf} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(
                                f"{year}/{pdf} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{year}/{pdf} was downloaded, it had response status code {response.status_code}")

    # The following method will check all the years on the archive
    def check_years(self):
        for year in self.years:
            self.check_year(year)

if __name__ == "__main__":
    namibian = TheNamibian()
    namibian.check_years()