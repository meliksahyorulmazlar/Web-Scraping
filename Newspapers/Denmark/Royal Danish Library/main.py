# Danish Royal Library
import datetime
import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class DanishRoyalLibrary:
    def __init__(self):
        self.newspaper_dictionary = {}
        self.current_year = self.get_year()
        self.start_webdriver()
        self.gather_newspapers()

    # The following method gets the current year
    def get_year(self):
        return datetime.datetime.now().year

    # The following method will  start the selenium webdriver
    def start_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method will gather all the newspapers on the archive
    def gather_newspapers(self):
        website = 'https://www2.statsbiblioteket.dk/mediestream/avis/list'
        self.driver.get(website)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source,'lxml')

        for newspaper in soup.find_all('a',href=True,class_='newspaper'):
            key = newspaper.text
            value = 'https://www2.statsbiblioteket.dk/mediestream/avis/' + newspaper['href']
            self.newspaper_dictionary[key] =  value

    # The following method will print the names of all the newspapers
    def print_names(self):
        for newspaper in self.newspaper_dictionary:
            print(newspaper)

    # The following method will download the names of all the newspapers starting with a specific letter
    def print_letter_names(self,letter:str):
        for newspaper in self.newspaper_dictionary:
            if newspaper[0].lower() == letter[0].lower():
                print(newspaper)

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            os.mkdir(newspaper)
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            # The newspaper has to be at least 100 years old
            # For example any newspaper in 1926 cannot be downloaded until 2026
            # Any newspaper from 1925 and before can be downloaded in 2025
            years = [int(year.text) for year in soup.find_all('a', href=True) if len(year.text) == 4 and year.text != 'Info']

            for year in years:
                if year +100 > self.current_year:
                    print(f"Year:{year}, it is not old enough")
                else:
                    year_site = f"{site}/{year}"
                    self.driver.get(year_site)
                    time.sleep(5)
                    soup = BeautifulSoup(self.driver.page_source,'lxml')
                    dates = [date['data-query'].split("*")[0].split(":")[-1] for date in soup.find_all('a', class_='query',attrs={"data-query":True})]
                    code = self.newspaper_dictionary[newspaper].split(":")[-1]
                    for date in dates:
                        filename = f"{date}.pdf"
                        if filename not in os.listdir(f"{newspaper}"):
                            day_website = f'https://www2.statsbiblioteket.dk/mediestream/avis/search/iso_dateTime:{date}* titleUUID:"doms_aviser_title:uuid:{code}"'
                            self.driver.get(day_website)
                            time.sleep(5)
                            soup = BeautifulSoup(self.driver.page_source,'lxml')
                            link = soup.find('a',href=True,class_='record')
                            self.driver.get(link['href'])
                            time.sleep(5)
                            soup = BeautifulSoup(self.driver.page_source,'lxml')
                            pdf_link = soup.find('a',href=True,class_='downloadPaperPDF')
                            response = requests.get(url=pdf_link['href'])
                            if response.status_code == 200:
                                with open(f"{newspaper}/{filename}",'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt','a') as f:
                                    f.write(f"{newspaper}/{filename} was downloaded.\n")
                                print(f"{newspaper}/{filename} was downloaded.")
                            else:
                                with open('download_results.txt','a') as f:
                                    f.write(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                                print(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method check a specific newspaper
    def check_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            # The newspaper has to be at least 100 years old
            # For example any newspaper in 1926 cannot be downloaded until 2026
            # Any newspaper from 1925 and before can be downloaded in 2025
            years = [int(year.text) for year in soup.find_all('a', href=True) if len(year.text) == 4 and year.text != 'Info']

            for year in years:
                if year +100 > self.current_year:
                    print(f"Year:{year}, it is not old enough")
                else:
                    year_site = f"{site}/{year}"
                    self.driver.get(year_site)
                    time.sleep(5)
                    soup = BeautifulSoup(self.driver.page_source,'lxml')
                    dates = [date['data-query'].split("*")[0].split(":")[-1] for date in soup.find_all('a', class_='query',attrs={"data-query":True})]
                    code = self.newspaper_dictionary[newspaper].split(":")[-1]
                    for date in dates:
                        day_website = f'https://www2.statsbiblioteket.dk/mediestream/avis/search/iso_dateTime:{date}* titleUUID:"doms_aviser_title:uuid:{code}"'
                        self.driver.get(day_website)
                        time.sleep(5)
                        soup = BeautifulSoup(self.driver.page_source,'lxml')
                        link = soup.find('a',href=True,class_='record')
                        self.driver.get(link['href'])
                        time.sleep(5)
                        soup = BeautifulSoup(self.driver.page_source,'lxml')
                        pdf_link = soup.find('a',href=True,class_='downloadPaperPDF')
                        filename = f"{date}.pdf"
                        if filename not in os.listdir(f"{newspaper}"):
                            response = requests.get(url=pdf_link['href'])
                            if response.status_code == 200:
                                with open(f"{newspaper}/{filename}",'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt','a') as f:
                                    f.write(f"{newspaper}/{filename} was downloaded.\n")
                                print(f"{newspaper}/{filename} was downloaded.")
                            else:
                                with open('download_results.txt','a') as f:
                                    f.write(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                                print(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the newspapers on the archive
    def download_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    # The following method will check all the newspapers on the archive
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

if __name__ == "__main__":
    drl = DanishRoyalLibrary()
    drl.download_newspapers()