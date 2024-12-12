# Radiocorriere Archive

import requests,os,lxml
from bs4 import BeautifulSoup


class Radiocorriere:
    def __init__(self):
        self.site = 'http://www.radiocorriere.teche.rai.it/Default.aspx'
        self.years = {}
        self.gather_years()

    #The following method will gather all the years on the archive
    def gather_years(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        times = [f"http://www.radiocorriere.teche.rai.it/{link['href']}" for link in soup.find_all('a',href=True) if 'data' in link['href']]

        for time in times:
            new_soup = BeautifulSoup(requests.get(url=time).text,'lxml')
            years = [year['href'] for year in new_soup.find_all('a',href=True) if 'Fascicoli' in year['href']]
            for y in years:
                key = int(y.split("=")[1])
                value = f"http://www.radiocorriere.teche.rai.it/{y}"
                self.years[key] = value


    #The following method will print all the valid years that are on the archive
    def print_years(self):
        for y in self.years:
            print(y)

    # The following method will download a specific year that is on the archive
    def download_year(self,year:int):
        if year in self.years:
            site = self.years[year]
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            new = [f"http://www.radiocorriere.teche.rai.it/{link['href']}" for link in soup.find_all('a',href=True) if f"{year}" in link['href']]
            pdfs= []
            for n in new:
                if n not in pdfs and 'Download' in n:
                    pdfs.append(n)
            print(pdfs)
            for p in pdfs:
                filename = p.split("=")[1]
                response = requests.get(url=p)
                if response.status_code == 200:
                    with open(f"{filename}.pdf",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename}.pdf was downloaded.\n")
                    print(f"{filename}.pdf was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename}.pdf was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename}.pdf was not downloaded,it had response status code {response.status_code}")

    #The following method will download all the years
    def download_years(self):
        for y in self.years:
            self.download_year(y)

    def check_year(self,year:int):
        if year in self.years:
            site = self.years[year]
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            new = [f"http://www.radiocorriere.teche.rai.it/{link['href']}" for link in soup.find_all('a', href=True) if f"{year}" in link['href']]
            pdfs = []
            for n in new:
                if n not in pdfs and 'Download' in n:
                    pdfs.append(n)
            for p in pdfs:
                filename = p.split("=")[1]
                if f"{filename}.pdf" not in os.listdir():
                    response = requests.get(url=p)
                    if response.status_code == 200:
                        with open(f"{filename}.pdf", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename}.pdf was downloaded.\n")
                        print(f"{filename}.pdf was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(
                                f"{filename}.pdf was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename}.pdf was not downloaded,it had response status code {response.status_code}")

    # The following method will check all the years
    def check_years(self):
        for y in self.years:
            self.check_year(y)

if __name__ == "__main__":
    radiocorriere = Radiocorriere()
    radiocorriere.check_years()