# L'Osservatore della Domenica  Archive
import datetime
import os
import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class LosservatoreDellaDomenica:
    def __init__(self):
        self.page = 'https://www.osservatoreromano.va/it/osservatore-della-domenica/archivio.html'
        self.start_driver()

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    # The followi
    def download_year(self,year:int):
        pdf_list = []
        for i in range(12):
            site = f'https://www.osservatoreromano.va/it/osservatore-della-domenica/archivio.html?q=Anno&from=01%2F{1+i}%2F{year}&to=31%2F{1+i}%2F{year}&in=all&sorting=relevance&year=#1'
            self.driver.get(site)
            time.sleep(2.5)
            if i+1 >= 10:
                string = f"{year}{i + 1}"
            else:
                string = f"{year}0{i + 1}"

            pdfs = [anchor.get_attribute('href') for anchor in self.driver.find_elements(By.TAG_NAME,'a') if anchor.get_attribute('href') and '.pdf.html' in anchor.get_attribute('href') and string in anchor.get_attribute('href')]
            while not pdfs:
                time.sleep(3)
                pdfs = [anchor.get_attribute('href') for anchor in self.driver.find_elements(By.TAG_NAME, 'a') if anchor.get_attribute('href') and '.pdf.html' in anchor.get_attribute('href') and string in anchor.get_attribute('href')]
            pdf_list += pdfs
        for pdf in pdf_list:
            filename = pdf.split("/")[-1]
            filename = filename.replace('.html','')
            website = f'https://media.osservatoreromano.va/media/osservatoreromano/odd/pdf/{filename}'
            response = requests.get(url=website)
            if response.status_code == 200:
                with open(f'{filename}','wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was downloaded.\n")
                print(f"{filename} was downloaded.")
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # This method will download all the years
    def download_years(self):
        for year in range(1934,2008):
            self.download_year(year)

    # This method will check if all the pdfs for a specific have been downloaded or not
    def check_year(self,year):
        pdf_list = []
        for i in range(12):
            site = f'https://www.osservatoreromano.va/it/osservatore-della-domenica/archivio.html?q=Anno&from=01%2F{1 + i}%2F{year}&to=31%2F{1 + i}%2F{year}&in=all&sorting=relevance&year=#1'
            self.driver.get(site)
            time.sleep(2.5)
            if i + 1 >= 10:
                string = f"{year}{i + 1}"
            else:
                string = f"{year}0{i + 1}"

            pdfs = [anchor.get_attribute('href') for anchor in self.driver.find_elements(By.TAG_NAME, 'a') if
                    anchor.get_attribute('href') and '.pdf.html' in anchor.get_attribute(
                        'href') and string in anchor.get_attribute('href')]
            while not pdfs:
                time.sleep(3)
                pdfs = [anchor.get_attribute('href') for anchor in self.driver.find_elements(By.TAG_NAME, 'a') if
                        anchor.get_attribute('href') and '.pdf.html' in anchor.get_attribute(
                            'href') and string in anchor.get_attribute('href')]
            pdf_list += pdfs
        for pdf in pdf_list:
            filename = pdf.split("/")[-1]
            filename = filename.replace('.html', '')
            if filename not in os.listdir():
                website = f'https://media.osservatoreromano.va/media/osservatoreromano/odd/pdf/{filename}'
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f'{filename}', 'wb') as f:
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
        for year in range(1934,2008):
            self.check_year(year)


if __name__ == "__main__":
    ldl = LosservatoreDellaDomenica()
    ldl.check_year(1935)