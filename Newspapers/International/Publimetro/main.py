# Publimetro
import os

import requests,lxml
from bs4 import BeautifulSoup


class Publimetro:
    def __init__(self):
        self.countries = []
        self.gather_countries()

    # The following method will gather all the countries on the archive
    def gather_countries(self):
        site = 'https://www.readmetro.com/es/'
        soup = BeautifulSoup(requests.get(url=site).text,'lxml')
        for c in soup.find_all('a',href=True,title=True):
            if c['href'].count("/")== 3 and 'http' not in c['href']:
                country = c['href'].split("/")[-2]
                if country not in self.countries:
                    self.countries.append(country)


    # The following method will download a particular country
    def download_country(self,country:str):
        if country in self.countries:
            os.mkdir(country)
            site = f'https://www.readmetro.com/es/{country}/'
            soup = BeautifulSoup(requests.get(site).text, 'lxml')
            cities = [city['href'].split("/")[-3] for city in soup.find_all('a', href=True) if 'archive' in city['href']]
            for city in cities:
                os.mkdir(f"{country}/{city}")
                archive_site = f"https://www.readmetro.com/es/{country}/{city}/archive/"
                new_soup = BeautifulSoup(requests.get(url=archive_site).text, 'lxml')
                days = [day['href'].split("/")[-2] for day in new_soup.find_all('a', href=True) if day['href'].count("/") == 5]
                for day in days:
                    year = day[0:4]
                    month = day[4:6]
                    day = day[6:]
                    pdf_link = f"https://rm.metrolatam.com/pdf/{year}/{month}/{day}/{year}{month}{day}_{city}.pdf"
                    print(pdf_link)
                    filename = pdf_link.split("/")[-1]
                    response = requests.get(url=pdf_link)
                    if response.status_code == 200:
                        with open(f"{country}/{city}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}.")


    # The following method will check a particular country
    def check_country(self, country: str):
        if country in self.countries:
            try:
                os.mkdir(country)
            except FileExistsError:
                pass
            site = f'https://www.readmetro.com/es/{country}/'
            soup = BeautifulSoup(requests.get(site).text, 'lxml')
            cities = [city['href'].split("/")[-3] for city in soup.find_all('a', href=True) if 'archive' in city['href']]

            for city in cities:
                try:
                    os.mkdir(f"{country}/{city}")
                except FileExistsError:
                    pass
                archive_site = f"https://www.readmetro.com/es/{country}/{city}/archive/"
                new_soup = BeautifulSoup(requests.get(url=archive_site).text, 'lxml')
                days = [day['href'].split("/")[-2] for day in new_soup.find_all('a', href=True) if
                        day['href'].count("/") == 5]
                for day in days:
                    year = day[0:4]
                    month = day[4:6]
                    day = day[6:]
                    pdf_link = f"https://rm.metrolatam.com/pdf/{year}/{month}/{day}/{year}{month}{day}_{city}.pdf"
                    print(pdf_link)
                    filename = pdf_link.split("/")[-1]
                    if filename not in os.listdir(f"{country}/{city}"):
                        response = requests.get(url=pdf_link)
                        if response.status_code == 200:
                            with open(f"{country}/{city}/{filename}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{filename} was downloaded.\n")
                            print(f"{filename} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{filename} was not downloaded, it had response status code {response.status_code}.")
                    else:
                        print(f"{filename} was already downloaded")


    # The following method will download all the countries
    def download_countries(self):
        for country in self.countries:
            self.download_country(country)

    # The following method will check all the countries
    def check_countries(self):
        for country in self.countries:
            self.check_country(country)

    # The following method will print all the countries that has publimetro
    def print_countries(self):
        for c in self.countries:
            print(c)

if __name__ == "__main__":
    publimetro = Publimetro()
    publimetro.check_countries()