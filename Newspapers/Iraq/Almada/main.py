# Almada, Iraqi Newspaper

import requests,os,lxml
from bs4 import BeautifulSoup


class Almada:
    def __init__(self):
        self.pages = self.gather_pages()

    # The following method will gather the page count
    def gather_pages(self)->int:
        website = 'https://almadapaper.net/file-sections/'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [int(page['href'].split("/")[-2]) for page in soup.find_all('a',href=True) if 'page' in page['href']]
        return max(pages)

    # The following method will print how many pages the archive has
    def print_page_count(self):
        print(self.pages)

    # The following method will download a specific page number
    def download_page_number(self,number:int):
        if 1 <= number <= self.pages:
            website = f'https://almadapaper.net/file-sections/page/{number}/'
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            files = [f"https://almadapaper.net{file['href']}" for file in soup.find_all('a',href=True) if 'file_section' in file['href']]
            files = files[1:]
            print(files)
            for file in files:
                pdf_soup = BeautifulSoup(requests.get(file).text,'lxml')
                pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                number = pdf_soup.find('h1').text.split(" ")[2]
                print(number)
                os.mkdir(number)
                for pdf in pdfs:
                    filename = pdf.split("/")[-1]
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{number}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{number}/{filename} was downloaded.\n")
                        print(f"{number}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{number}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{number}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one number to another later page number
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for page in range(n1,n2+1):
            self.download_page_number(page)

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(1,self.pages)


    # The following method will check a specific page number
    def check_page_number(self,number:int):
        if 1 <= number <= self.pages:
            website = f'https://almadapaper.net/file-sections/page/{number}/'
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            files = [f"https://almadapaper.net{file['href']}" for file in soup.find_all('a',href=True) if 'file_section' in file['href']]
            files = files[1:]
            print(files)
            for file in files:
                pdf_soup = BeautifulSoup(requests.get(file).text,'lxml')
                pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                number = pdf_soup.find('h1').text.split(" ")[2]
                print(number)
                try:
                    os.mkdir(number)
                except FileExistsError:
                    pass
                for pdf in pdfs:
                    filename = pdf.split("/")[-1]
                    if filename not in os.listdir(number):
                        response = requests.get(pdf)
                        if response.status_code == 200:
                            with open(f"{number}/{filename}",'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt','a') as f:
                                f.write(f"{number}/{filename} was downloaded.\n")
                            print(f"{number}/{filename} was downloaded.")
                        else:
                            with open('download_results.txt','a') as f:
                                f.write(f"{number}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{number}/{filename} was not downloaded, it had response status code {response.status_code}")
                    else:
                        print(f"{filename} was already downloaded")

    # The following method will check from one number to another later page number
    def check_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for page in range(n1, n2 + 1):
            self.check_page_number(page)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(1,self.pages)

if __name__ == "__main__":
    almada = Almada()
    almada.check_all()