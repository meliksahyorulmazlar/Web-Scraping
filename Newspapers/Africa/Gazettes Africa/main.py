# Gazettes Africa webscraper
# An archive of government gazettes of African

import requests,os,lxml
from bs4 import BeautifulSoup


class GazettesAfrica:
    def __init__(self):
        self.main_page = 'https://gazettes.africa'
        self.country_dictionary = {}
        self.gather_countries()

    # This gathers all the countries on the archive
    def gather_countries(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        countries = [(link.text.strip(),f"{link['href']}") for link in soup.find_all('a',href=True) if 'gazettes' in link['href']]

        for c in countries:
            self.country_dictionary[c[0]] = c[1]

    # This method downloads all the newspapers for a particular African country
    def download_country(self,country):
        if country in self.country_dictionary:
            link = f'https://gazettes.africa{self.country_dictionary[country]}'
            soup = BeautifulSoup(requests.get(url=link).text,'lxml')
            year_links = [year['href'] for year in soup.find_all('a',href=True) if self.country_dictionary[country] in year['href'] and "#" not in year['href']]
            years = []
            for y in year_links:
                string = y.split("/")
                if string[3] != '':
                    years.append(f"https://gazettes.africa{y}")
            years.sort()
            for year in years:
                year_int = year.split("/")[-1]
                print(year_int)
                year_soup = BeautifulSoup(requests.get(url=year).text,'lxml')
                papers = [f"https://gazettes.africa{p['href']}" for p in year_soup.find_all('a',href=True) if 'government-gazette' in p['href']]
                print(papers)
                for p in papers:
                    paper_soup = BeautifulSoup(requests.get(url=p).text,'lxml')
                    h1 = paper_soup.find('h1').text
                    country_code = self.country_dictionary[country].split("/")[-2]
                    h1 = h1.replace(country,country_code)
                    h1 = h1.lower().replace(" ","-")
                    h1 = h1.replace('number','no')
                    pdf_link = f"https://archive.gazettes.africa/archive/{country_code}/{year_int}/{h1}.pdf"
                    try:
                        os.mkdir(country)
                    except FileExistsError:
                        pass

                    try:
                        os.mkdir(f"{country}/{year_int}")
                    except FileExistsError:
                        pass

                    response = requests.get(url=pdf_link)
                    filename = h1
                    if response.status_code == 200:
                        with open(f'{country}/{year_int}/{filename}.pdf','wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{country}/{year_int}/{filename}.pdf was downloaded\n")
                        print(f'{country}/{year_int}/{filename}.pdf was downloaded')
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{country}/{year_int}/{filename}.pdf was not downloaded, it had response status code {response.status_code}\n")
                        print(f'{country}/{year_int}/{filename}.pdf was not downloaded, it had response status code {response.status_code}')

    # The following method will download all the countries on the archive
    def download_countries(self):
        for c in self.country_dictionary:
            self.download_country(c)

    # The following method will check if there are any missing newspapers that have been added or not downloaded and it will download them
    def check_country(self,country:str):
        if country in self.country_dictionary:
            link = f'https://gazettes.africa{self.country_dictionary[country]}'
            soup = BeautifulSoup(requests.get(url=link).text, 'lxml')
            year_links = [year['href'] for year in soup.find_all('a', href=True) if
                          self.country_dictionary[country] in year['href'] and "#" not in year['href']]
            years = []
            for y in year_links:
                string = y.split("/")
                if string[3] != '':
                    years.append(f"https://gazettes.africa{y}")
            years.sort()
            for year in years:
                year_int = year.split("/")[-1]
                print(year_int)
                year_soup = BeautifulSoup(requests.get(url=year).text, 'lxml')
                papers = [f"https://gazettes.africa{p['href']}" for p in year_soup.find_all('a', href=True) if 'government-gazette' in p['href']]
                print(papers)
                for p in papers:
                    paper_soup = BeautifulSoup(requests.get(url=p).text, 'lxml')
                    h1 = paper_soup.find('h1').text
                    country_code = self.country_dictionary[country].split("/")[-2]
                    h1 = h1.replace(country, country_code)
                    h1 = h1.lower().replace(" ", "-")
                    h1 = h1.replace('number', 'no')
                    pdf_link = f"https://archive.gazettes.africa/archive/{country_code}/{year_int}/{h1}.pdf"
                    try:
                        os.mkdir(country)
                    except FileExistsError:
                        pass
                    try:
                        os.mkdir(f"{country}/{year_int}")
                    except FileExistsError:
                        pass
                    filename = h1
                    if f"{filename}.pdf" not in os.listdir(f"{country}/{year_int}"):
                        response = requests.get(url=pdf_link)

                        if response.status_code == 200:
                            with open(f'{country}/{year_int}/{filename}.pdf', 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{country}/{year_int}/{filename}.pdf was downloaded\n")
                            print(f'{country}/{year_int}/{filename}.pdf was downloaded')
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{country}/{year_int}/{filename}.pdf was not downloaded, it had response status code {response.status_code}\n")
                            print(f'{country}/{year_int}/{filename}.pdf was not downloaded, it had response status code {response.status_code}')

    # The following method will check all the countries on the archive
    def check_countries(self):
        for c in self.country_dictionary:
            self.check_country(c)

if __name__ == "__main__":
    ga = GazettesAfrica()
    ga.download_countries()