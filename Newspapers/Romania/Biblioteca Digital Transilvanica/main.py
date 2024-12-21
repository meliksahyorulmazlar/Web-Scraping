#Biblioteca Digital Transilvanica

import requests,os,lxml
from bs4 import BeautifulSoup

class BibliotecaDigitalTransilvanica:
    def __init__(self):
        self.main_page = 'https://documente.bcucluj.ro/periodice.html'
        self.newspapers = {}
        self.gather_newspapers()

    # The following method will gather all the newspapers
    def gather_newspapers(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        for link in soup.find_all('a',href=True):
            if 'periodice' in link['href'] and 'pdf' not in link['href']:
                key = link.text
                value = f'https://documente.bcucluj.ro/{link["href"]}'
                self.newspapers[key] = value

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            os.mkdir(f"{newspaper}")
            site = self.newspapers[newspaper]
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            years = [f"{site}{year['href']}"for year in soup.find_all('a',href=True) if 'html' in year['href'] and 'periodice.html' not in year['href']]
            for year in years:
                year_str = year.split("/")[-1].replace(".html",'')
                try:
                    os.mkdir(f"{newspaper}/{year_str}")
                except FileExistsError:
                    pass
                newspaper_name = year.split('/')[-2]
                year_soup = BeautifulSoup(requests.get(url=year).text,'lxml')
                pdfs = [pdf['href'] for pdf in year_soup.find_all('a',href=True) if 'pdf' in pdf['href']]
                for pdf in pdfs:
                    pdf_code = pdf.split("/")[-1]
                    pdf_link = f'https://documente.bcucluj.ro/web/bibdigit/periodice/{newspaper_name}/{year_str}/{pdf_code}'

                    response = requests.get(url=pdf_link)
                    if response.status_code == 200:
                        with open(f"{newspaper}/{year_str}/{pdf_code}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{newspaper}/{year_str}/{pdf_code} was downloaded.\n")
                        print(f"{newspaper}/{year_str}/{pdf_code} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{newspaper}/{year_str}/{pdf_code} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{newspaper}/{year_str}/{pdf_code} was not downloaded, it had response status code {response.status_code}")


    # The following method will download all the newspapers on the archive
    def download_newspapers(self):
        for newspaper in self.newspapers:
            self.download_newspaper(newspaper)

    # The following method will check if all the pdfs for a specific newspaper has been downloaded or not
    def check_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            try:
                os.mkdir(f"{newspaper}")
            except FileExistsError:
                pass
            site = self.newspapers[newspaper]
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            years = [f"{site}{year['href']}" for year in soup.find_all('a', href=True) if
                     'html' in year['href'] and 'periodice.html' not in year['href']]
            for year in years:
                year_str = year.split("/")[-1].replace(".html", '')
                try:
                    os.mkdir(f"{newspaper}/{year_str}")
                except FileExistsError:
                    pass
                newspaper_name = year.split('/')[-2]
                year_soup = BeautifulSoup(requests.get(url=year).text, 'lxml')
                pdfs = [pdf['href'] for pdf in year_soup.find_all('a', href=True) if 'pdf' in pdf['href']]
                for pdf in pdfs:
                    pdf_code = pdf.split("/")[-1]
                    if pdf_code not in os.listdir(f"{newspaper}/{year_str}"):
                        pdf_link = f'https://documente.bcucluj.ro/web/bibdigit/periodice/{newspaper_name}/{year_str}/{pdf_code}'
                        response = requests.get(url=pdf_link)
                        if response.status_code == 200:
                            with open(f"{newspaper}/{year_str}/{pdf_code}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{newspaper}/{year_str}/{pdf_code} was downloaded.\n")
                            print(f"{newspaper}/{year_str}/{pdf_code} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{newspaper}/{year_str}/{pdf_code} was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{newspaper}/{year_str}/{pdf_code} was not downloaded, it had response status code {response.status_code}")

    # The following method will check all the newspapers for if all the newspapers have been downloaded or not
    def check_newspapers(self):
        for newspaper in self.newspapers:
            self.check_newspaper(newspaper)

    # The following method will print the names of all the newspaper
    def print_names(self):
        for newspaper in self.newspapers:
            print(newspaper)

if __name__ == "__main__":
    bdt = BibliotecaDigitalTransilvanica()
    bdt.check_newspaper(newspaper='Abecedar (1933-1934)')
