import os,time
import shutil

import requests
import selenium.common.exceptions
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
class AlWasatBahrain:
    def __init__(self):
        self.minimum = 1
        self.maximum = 5384
        self.base_url = "http://www.alwasatnews.com/pdf/"
        self.driver = uc.Chrome()

    # The following number will download a specific number
    def download_number(self, number: int):
        if self.minimum <= number <= self.maximum:
            os.mkdir(f"{number}")
            page = f"{self.base_url}index.php?issue={number+1}&cat=ads"
            self.driver.get(page)
            try:
                self.driver.switch_to.frame(0)
            except selenium.common.exceptions.NoSuchFrameException:
                shutil.rmtree(f'{number}')
                print(f"This number had none")
            else:
                soup = BeautifulSoup(self.driver.page_source,'lxml')
                pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                for pdf in pdfs:
                    pdf_link = 'http://www.alwasatnews.com/pdf/' + pdf.replace("?2015",'')
                    pdf = pdf_link.split("/")[-1]
                    response = requests.get(pdf_link)
                    if response.status_code == 200:
                        with open(f"{number}/{pdf}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{number}/{pdf} was downloaded.\n")
                        print(f"{number}/{pdf} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{number}/{pdf} was not downloaded, it had response status code {response.status_code}")
                        print(f"{number}/{pdf} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one number to another later number
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n1 = c

        for i in range(n1,n2+1):
            self.download_number(i)

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(self.minimum,self.maximum)

    # The following number will download a specific number
    def check_number(self, number: int):
        if self.minimum <= number <= self.maximum:
            try:
                os.mkdir(f"{number}")
            except FileExistsError:
                pass
            page = f"{self.base_url}index.php?issue={number + 1}&cat=ads"
            self.driver.get(page)
            try:
                self.driver.switch_to.frame(0)
            except selenium.common.exceptions.NoSuchFrameException:
                shutil.rmtree(f'{number}')
                print(f"This number had none")
            else:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
                for pdf in pdfs:
                    pdf_link = 'http://www.alwasatnews.com/pdf/' + pdf.replace("?2015", '')
                    pdf = pdf_link.split("/")[-1]
                    if pdf not in os.listdir(f"{number}"):
                        response = requests.get(pdf_link)
                        if response.status_code == 200:
                            with open(f"{number}/{pdf}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{number}/{pdf} was downloaded.\n")
                            print(f"{number}/{pdf} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(
                                    f"{number}/{pdf} was not downloaded, it had response status code {response.status_code}")
                            print(f"{number}/{pdf} was not downloaded, it had response status code {response.status_code}")
                    else:
                        print(f"{number}/{pdf} was already downloaded.")

    # The following method will check from one number to another later number
    def check_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n1 = c

        for i in range(n1, n2 + 1):
            self.check_number(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(self.minimum, self.maximum)

if __name__ == "__main__":
    al_wasat = AlWasatBahrain()
    # al_wasat.download_n1_n2(1,2)
    al_wasat.check_n1_n2(1,3)