# Trintity News
import os

import requests,lxml
from bs4 import BeautifulSoup

class TrinityNews:
    def __init__(self):
        self.site = 'http://www.trinitynewsarchive.ie/pdf/'
        self.check_newspapers()

    #The following method will download all the newspapers
    def download_newspapers(self):
        soup = BeautifulSoup(requests.get(url=self.site).text, 'lxml')
        pdfs = [link['href'] for link in soup.find_all('a', href=True) if 'pdf' in link['href']]
        for pdf in pdfs:
            link = 'http://www.trinitynewsarchive.ie/pdf/01-01.pdf'
            response = requests.get(url=link)
            if response.status_code == 200:
                with open(pdf, 'wb') as f:
                    f.write(response.content)
                with open('download_results.txt', 'a') as f:
                    f.write(f"{pdf} was downloaded.\n")
                print(f"{pdf} was downloaded.")
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(f"{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                print(f"{pdf} was not downloaded., it had response status code {response.status_code}.")

    # The following method will download the newspapers that have not been downloaded
    def check_newspapers(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        pdfs = [link['href'] for link in soup.find_all('a',href=True) if 'pdf' in link['href']]
        for pdf in pdfs:
            link = 'http://www.trinitynewsarchive.ie/pdf/01-01.pdf'
            if pdf not in os.listdir():
                response = requests.get(url=link)
                if response.status_code == 200:
                    with open(pdf,'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{pdf} was downloaded.\n")
                    print(f"{pdf} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{pdf} was not downloaded., it had response status code {response.status_code}.")

if __name__ == "__main__":
    tn = TrinityNews()
