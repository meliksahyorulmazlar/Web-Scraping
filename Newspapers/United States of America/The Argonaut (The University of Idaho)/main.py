# The Argonaut (The University of Idaho) student newspaper archive

import requests,os,lxml
from bs4 import BeautifulSoup


class Argonaut:
    def __init__(self):
        self.site = 'https://www.lib.uidaho.edu/digital/argonaut/timeline.html'
        self.years = {}
        self.gather_papers()

    #The following method will gather all the newspapers
    def gather_papers(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        links = [f"https://www.lib.uidaho.edu{link['href']}" for link in soup.find_all('a',href=True) if '/digital/argonaut/items/a' in link['href']]

        for link in links:
            year = int(link.split("-")[1])
            if year in self.years:
                self.years[year].append(link)
            else:
                self.years[year] = [link]

    #The following method will download all the pdfs for a specific year if it is on the archive
    def download_year(self,year:int):
        if year in self.years:
            os.mkdir(f"{year}")
            pdfs = self.years[year]
            for pdf in pdfs:
                filename = pdf.replace("html", 'pdf').split("/")[-1]
                new_link = f"https://objects.lib.uidaho.edu/argonaut/pdf/{filename}"
                response = requests.get(url=new_link)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{year}/{filename} was not downloaded,it had response status code {response.status_code}")

    #The following method will download all the years on the archive
    def download_years(self):
        for year in self.years:
            self.download_year(year)

    #The following method will check if all the pdfs for a specific year have been downloaded or nor
    def check_year(self,year:int):
        if year in self.years:
            os.mkdir(f"{year}")
            pdfs = self.years[year]
            for pdf in pdfs:
                filename = pdf.replace("html", 'pdf').split("/")[-1]
                if filename not in os.listdir(f"{year}"):
                    new_link = f"https://objects.lib.uidaho.edu/argonaut/pdf/{filename}"
                    response = requests.get(url=new_link)
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

    #The following method will check the pdfs for all the years
    def check_years(self):
        for year in self.years:
            self.check_year(year)

    #The following method will print all the years on the archive
    def print_years(self):
        for year in self.years:
            print(year)

if __name__ == "__main__":
    argonaut = Argonaut()
    argonaut.download_years()
