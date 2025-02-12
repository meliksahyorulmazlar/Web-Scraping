# La Gazette des Comores, is a Newspaper from Comoros

import requests,lxml,os
from bs4 import BeautifulSoup


class LaGazettedesComores:
    def __init__(self):
        self.pages = self.return_page_count()

    # The following method will gather the page count
    def return_page_count(self):
        website = 'https://lagazettedescomores.com/journal-en-pdf/'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [int(page['href'].split("=")[-1]) for page in soup.find_all('a',href=True) if 'journal-en-pdf/?' in page['href']]
        return max(pages)

    # The following method will print how many pages the website has
    def print_page_count(self):
        print(self.pages)

    # The following method will download a specific page number
    def download_page(self,number:int):
        if 1 <= number <= self.pages:
            website = f'https://lagazettedescomores.com/journal-en-pdf/?page={number}'
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            files = [(pdf.text,f"https://lagazettedescomores.com/{pdf['href']}") for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            for file in files:
                filename = f"{file[0]}.pdf".replace("/",'-')
                print(file[1])
                response = requests.get(file[1])
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{filename} was downloaded, it had response status code {response.status_code}.")

    # The following method download from one page to another later page
    def download_page_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for n in range(n1,n2+1):
            self.download_page(n)

    # The following method will download the entire archive
    def download_all(self):
        self.download_page_n1_n2(1,self.pages)

    # The following method will check a particular page
    def check_page(self,number:int):
        if 1 <= number <= self.pages:
            website = f'https://lagazettedescomores.com/journal-en-pdf/?page={number}'
            soup = BeautifulSoup(requests.get(website).text, 'lxml')
            files = [(pdf.text, f"https://lagazettedescomores.com/{pdf['href']}") for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
            for file in files:
                filename = f"{file[0]}.pdf".replace("/", '-')
                if filename not in os.listdir():
                    print(file[1])
                    response = requests.get(file[1])
                    if response.status_code == 200:
                        with open(f"{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                        print(f"{filename} was downloaded, it had response status code {response.status_code}.")
                else:
                    print(f"{filename} was already downloaded")

    # The following method check from one page to another later page
    def check_page_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for n in range(n1,n2+1):
            self.check_page(n)

    # The following method will check the entire archive
    def check_all(self):
        self.check_page_n1_n2(1,self.pages)

if __name__ == "__main__":
    lgc = LaGazettedesComores()
    lgc.check_all()