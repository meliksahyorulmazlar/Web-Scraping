# Alik, Armenian Newspaper in Iran
import time

import requests,selenium,os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class Alik:
    def __init__(self):
        self.main_page = 'https://alikonline.ir/newspaper?cp=1'
        self.start_driver()
        self.pages = self.return_pagecount()


    # The following method will initiate the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)


    # The following method will find how many pages there are on the website
    def return_pagecount(self)->int:
        self.driver.get(self.main_page)
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        pages = [int(page['href'].split("=")[-1]) for page in soup.find_all('a',href=True) if "cp" in page['href']]
        return max(pages)

    # The following method will print how many pages there are
    def print_pages(self):
        print(self.pages)

    # The following method will download all the issues for a particular page
    def download_page(self,page_number:int):
        if 1 <= page_number <= self.pages:
            website = f"https://alikonline.ir/newspaper?cp={page_number}"
            self.driver.get(website)
            'https://alikonline.ir/download/pdf-20230801?wpdmdl=400&_wpdmkey=67ec56be12d50'
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if "download/pdf" in pdf['href']]
            for pdf in pdfs:
                if pdf.count("-") == 1:
                    date = pdf.split("-")[-1]
                    self.driver.get(f"https://alikonline.ir/{pdf}")
                    while True:
                        try:
                            download_button = self.driver.find_element(By.CLASS_NAME, 'wpdm-download-link')
                        except selenium.common.exceptions.NoSuchElementException:
                            continue
                        else:
                            break
                    download_link = download_button.get_attribute('data-downloadurl')
                    if download_link is not None:
                        response = requests.get(download_link)
                        if response.status_code == 200:
                            with open(f"{date}.pdf",'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt','a') as f:
                                f.write(f"{date}.pdf was downloaded.\n")
                            print(f"{date}.pdf was downloaded.")
                        else:
                            with open('download_results.txt','a') as f:
                                f.write(f"{date}.pdf was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{date}.pdf was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one page to another later page
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for page in range(n1,n2+1):
            self.download_page(page)

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(1,self.pages)

    # The following method will check a particular page if the pdfs for that page have been downloaded or not
    def check_page(self,page_number:int):
        if 1 <= page_number <= self.pages:
            website = f"https://alikonline.ir/newspaper?cp={page_number}"
            self.driver.get(website)

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if "download/pdf" in pdf['href']]
            for pdf in pdfs:
                if pdf.count("-") == 1 :
                    date = pdf.split("-")[-1]
                    print(pdf)
                    if f"{date}.pdf" not in os.listdir():
                        self.driver.get(f"https://alikonline.ir/{pdf}")
                        while True:
                            try:
                                download_button = self.driver.find_element(By.CLASS_NAME, 'wpdm-download-link')
                            except selenium.common.exceptions.NoSuchElementException:
                                continue
                            else:
                                break
                        download_link = download_button.get_attribute('data-downloadurl')
                        if download_link is not None:
                            response = requests.get(download_link)
                            if response.status_code == 200:
                                with open(f"{date}.pdf",'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt','a') as f:
                                    f.write(f"{date}.pdf was downloaded.\n")
                                print(f"{date}.pdf was downloaded.")
                            else:
                                with open('download_results.txt','a') as f:
                                    f.write(f"{date}.pdf was not downloaded, it had response status code {response.status_code}\n")
                                print(f"{date}.pdf was not downloaded, it had response status code {response.status_code}")
                    else:
                        print(f"{date}.pdf was already downloaded")

    # The following method will check from one page to another later page
    def check_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for page in range(n1, n2 + 1):
            self.check_page(page)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(1, self.pages)


if __name__ == "__main__":
    alik = Alik()
    alik.check_all()