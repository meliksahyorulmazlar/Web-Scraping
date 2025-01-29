# Gorenjski Glas

import requests,os,lxml
from bs4 import BeautifulSoup


class GorenjskiGlas:
    def __init__(self):
        old_archive = 'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=digitar&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page=1'
        self.old_count = self.find_number(old_archive)
        print(f"The old archive has {self.old_count} pages")
        new_archive = 'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=virtual&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page=1'
        self.new_count = self.find_number(new_archive)
        print(f"The new archive has {self.new_count} pages")

    # The following method will find the number of pages of the particular archive
    def find_number(self,site:str):
        soup = BeautifulSoup(requests.get(url=site).text,'lxml')
        pages = [int(page['href'].split('=')[-1]) for page in soup.find_all('a', href=True) if'page' in page['href'] and 'facebook' not in page['href']]
        return max(pages)


    # The following method will download a page number from the old archive
    # The following method will download a page number from 1948-2008 archive keyword = digitar
    def download_old_page(self,number:int):
        if number >= 1 and number <= self.old_count:
            page = f'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=digitar&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page={number}'
            soup = BeautifulSoup(requests.get(url=page).text,'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if 'pdf' in pdf['href']]
            pdfs = pdfs[1:]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                website = f'https://arhiv.gorenjskiglas.si{pdf}'
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download a page number from the new archive
    # The following method will download a page number from 2008-2024 archive keyword = virtual
    def download_new_page(self,number:int):
        if number >= 1 and number <= self.new_count:
            page = f'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=virtual&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page={number}'
            soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
            soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if 'pdf' in pdf['href']]
            pdfs = pdfs[1:]
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                website = f'https://arhiv.gorenjskiglas.si{pdf}'
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the pages from n1 to a later n2 (From the old archive)
    def download_old_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for page in range(n1,n2+1):
            self.download_old_page(page)

    # The following method will download all the pages from n1 to a later n2 (From the new archive)
    def download_new_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for page in range(n1, n2 + 1):
            self.download_new_page(page)

    # The following method will download the entire old archive
    def download_all_old(self):
        self.download_old_n1_n2(1, self.old_count)

    # The following method will download the entire new archive
    def download_all_new(self):
        self.download_new_n1_n2(1,self.new_count)

    # The following method will check the page of an old archive
    def check_old_page(self,number:int):
        page = f'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=digitar&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page={number}'
        soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if 'pdf' in pdf['href']]
        pdfs = pdfs[1:]
        for pdf in pdfs:
            filename = pdf.split("/")[-1]
            if filename not in os.listdir():
                website = f'https://arhiv.gorenjskiglas.si{pdf}'
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{filename}", 'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will check the page of a new archive
    def check_new_page(self,number:int):
        page = f'https://arhiv.gorenjskiglas.si/?FilterFromDate=&FilterToDate=&database=virtual&iskanje=&datefrom=&datefrom_submit=&dateto=&dateto_submit=&page={number}'
        soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
        soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if 'pdf' in pdf['href']]
        pdfs = pdfs[1:]
        for pdf in pdfs:
            filename = pdf.split("/")[-1]
            if filename not in os.listdir():
                website = f'https://arhiv.gorenjskiglas.si{pdf}'
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{filename}", 'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will check from n1 to a later n2 from the old archive
    def check_old_n1_n2(self,n1:int,n2:int):
        for page in range(1,self.old_count):
            self.download_old_page(page)

    # The following method will check from n1 to a later n2 from the old archive
    def check_new_n1_n2(self, n1: int, n2: int):
        for page in range(1, self.new_count):
            self.download_new_page(page)

if __name__ == "__main__":
    gg = GorenjskiGlas()
    gg.download_all_old()
