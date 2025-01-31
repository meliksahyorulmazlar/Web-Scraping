#الوطن Al Watan
import os

import requests,lxml
from bs4 import BeautifulSoup

class AlWatan:
    def __init__(self):
        self.pages = self.return_page_count()

    # The following method will print out how many pages the archive has
    def print_page_count(self):
        print(self.pages)

    # The following method will find how pages there are on the archive
    def return_page_count(self):
        soup = BeautifulSoup(requests.get(url='https://alwatan.sy/archives/category/newspaper').text,'lxml')
        pages = [int(page['href'].split("/")[-1]) for page in soup.find_all('a',href=True) if 'page' in page['href']]
        return max(pages)

    # The following method will download a particular page on the archive
    def download_page(self,number:int):
        if 1 <= number <= self.pages:
            site = f'https://alwatan.sy/archives/category/newspaper/page/{number}'
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            archive_numbers = [archive['href'].split("/")[-1] for archive in soup.find_all('a',href=True,class_='post-thumb')]
            for num in archive_numbers:
                os.mkdir(num)
                site = f'https://alwatan.sy/archives/{num}'
                soup = BeautifulSoup(requests.get(url=site).text,'lxml')
                pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                for pdf in pdfs:
                    filename = pdf.split("/")[-1]
                    pdf_link = f"https://alwatan.sy/{pdf}"

                    response = requests.get(url=pdf_link)
                    if response.status_code == 200:
                        with open(f"{num}/{filename}","wb") as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{num}/{filename} was downloaded.\n")
                        print(f"{num}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{num}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                        print(f"{num}/{filename} was not downloaded, it had response status code {response.status_code}.")

    # The following method will download from one page number to another later page number
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download_page(i)

    # The following method will download all the pages on the archive
    def download_pages(self):
        self.download_n1_n2(1,self.pages)


    # The following method will check a particular page on the archive
    def check_page(self,number:int):
        if 1 <= number <= self.pages:
            site = f'https://alwatan.sy/archives/category/newspaper/page/{number}'
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            archive_numbers = [archive['href'].split("/")[-1] for archive in
                               soup.find_all('a', href=True, class_='post-thumb')]
            for num in archive_numbers:
                try:
                    os.mkdir(num)
                except FileExistsError:
                    pass
                site = f'https://alwatan.sy/archives/{num}'
                soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
                pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
                for pdf in pdfs:
                    filename = pdf.split("/")[-1]
                    if filename not in os.listdir(f"{num}"):
                        pdf_link = f"https://alwatan.sy/{pdf}"
                        print(pdf_link)
                        response = requests.get(url=pdf_link)
                        if response.status_code == 200:
                            with open(f"{num}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{num}/{filename} was downloaded.\n")
                            print(f"{num}/{filename} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(
                                    f"{num}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                            print(
                                f"{num}/{filename} was not downloaded, it had response status code {response.status_code}.")

    # The following method will download from one page number to another later page number
    def check_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1, n2 + 1):
            self.check_page(i)

    # The following method will check all the pages on the archive
    def check_pages(self):
        self.check_n1_n2(1,self.pages)

if __name__ == "__main__":
    alwatan = AlWatan()
    alwatan.check_pages()