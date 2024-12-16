# Délmagyarország webscraper

import requests,os,lxml
from bs4 import BeautifulSoup


class Delmagyarorszag:
    def __init__(self):
        self.main_page = 'https://dmarchiv.bibl.u-szeged.hu/view/full_volume/newspaper/'
        self.year_dictionary = {}
        self.gather_data()

    #The following method will gather the data on the archive
    def gather_data(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        years = [link['href'] for link in soup.find_all('a',href=True) if '.html' in link['href'] and '/' not in link['href']]
        for y in years:
            key = int(y.replace(".html",''))
            value = f"https://dmarchiv.bibl.u-szeged.hu/view/full_volume/newspaper/{y}"
            self.year_dictionary[key] = value

    # The following method will download a specific year that is on the archive
    def download_year(self,year:int):
        if year in self.year_dictionary:
            os.mkdir(f"{year}")
            site = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            links = []
            for n in soup.find_all('a',href=True):
                if n['href'].count("/") == 4:
                    if len(n['href'].split("/")[-2]) == 5:
                        links.append(n['href'])
            for i in range(len(links)):
                site = 'http://dmarchiv.bibl.u-szeged.hu/11823/'
                link = links[i]
                count_string = ""
                number = i+1
                if number >= 100:
                    count_string = f"{number}"
                elif number >= 10:
                    count_string = f"0{number}"
                else:
                    count_string = f"00{number}"
                pdf_link = f'{link}/1/dm_{year}_{count_string}.pdf'
                filename = pdf_link.split("/")[-1]
                response = requests.get(url=pdf_link)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}.")

    # The following method will download all the years
    def download_years(self):
        for y in self.year_dictionary:
            self.download_year(y)

    # The following method will check if all the pdfs for that year
    def check_year(self,year:int):
        if year in self.year_dictionary:
            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass
            site = self.year_dictionary[year]
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            links = []
            for n in soup.find_all('a',href=True):
                if n['href'].count("/") == 4:
                    if len(n['href'].split("/")[-2]) == 5:
                        links.append(n['href'])
            for i in range(len(links)):
                site = 'http://dmarchiv.bibl.u-szeged.hu/11823/'
                link = links[i]
                count_string = ""
                number = i+1
                if number >= 100:
                    count_string = f"{number}"
                elif number >= 10:
                    count_string = f"0{number}"
                else:
                    count_string = f"00{number}"
                pdf_link = f'{link}/1/dm_{year}_{count_string}.pdf'
                filename = pdf_link.split("/")[-1]
                if filename not in os.listdir(f"{year}"):
                    response = requests.get(url=pdf_link)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                        print(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}.")

    #The following method will print all the years on the archive
    def print_years(self):
        for y in self.year_dictionary:
            print(y)

    #The following method will check all the years on the archive
    def check_years(self):
        for year in self.year_dictionary:
            self.check_year(year)
            
if __name__ == "__main__":
    delmagyarorszag = Delmagyarorszag()
    delmagyarorszag.check_year(1950)

