#La Voix de Djibouti


import requests,os,lxml
from bs4 import BeautifulSoup
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By


class LaVoixDeDjibouti:
    def __init__(self):
        self.page_count = self.return_page_count()


    # # The following method will start the selenium webdriver
    # def start_selenium_driver(self):
    #     options = webdriver.ChromeOptions()
    #     options.add_experimental_option('detach',True)
    #     # options.add_argument('--headless')
    #     self.driver = webdriver.Chrome(options=options)

    # The following method will return the page count
    def return_page_count(self):
        website = 'http://lavoixdedjibouti.info/category/editions-ecrites/'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [int(page['href'].split("/")[-2]) for page in soup.find_all('a',href=True) if 'page' in page['href']]
        return max(pages)

    # The following method will print how many pages there are on the archive
    def print_page_count(self):
        print(self.page_count)

    # The following method will download a particular page number
    def download_page(self,number:int):
        if 1 <= number <= self.page_count:
            pdfs = []
            website = f"https://lavoixdedjibouti.info/category/editions-ecrites/page/{number}/"
            soup = BeautifulSoup(requests.get(website).text, 'lxml')
            for pdf in soup.find_all('a', href=True):
                if 'edition-ecrite' in pdf['href'] and pdf['href'] not in pdfs:
                    pdfs.append(pdf['href'])
            for pdf in pdfs:
                new_soup = BeautifulSoup(requests.get(pdf).text,'lxml')
                link = new_soup.find('iframe',src=True)
                website = unquote(link['src'].split("file=")[-1])
                filename = website.split("/")[-1]

                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one page to another later page
    def download_p1_p2(self,p1:int,p2:int):
        if p1 > p2:
            c = p1
            p1 = p2
            p2 = c

        for page in range(p1,p2+1):
            self.download_page(page)

    # The following method will download the entire archive
    def download_all(self):
        self.download_p1_p2(1,self.page_count)

    # The following method will check a particular page number
    def check_page(self, number: int):
        if 1 <= number <= self.page_count:
            pdfs = []
            website = f"https://lavoixdedjibouti.info/category/editions-ecrites/page/{number}/"
            soup = BeautifulSoup(requests.get(website).text, 'lxml')
            for pdf in soup.find_all('a', href=True):
                if 'edition-ecrite' in pdf['href'] and pdf['href'] not in pdfs:
                    pdfs.append(pdf['href'])
            for pdf in pdfs:
                new_soup = BeautifulSoup(requests.get(pdf).text, 'lxml')
                link = new_soup.find('iframe', src=True)
                website = unquote(link['src'].split("file=")[-1])
                filename = website.split("/")[-1]
                pdfs = [pdf['href'] for pdf in new_soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                if '.pdf' not in filename and pdfs:
                    website = pdfs[0]
                    print(pdfs)
                    filename = website.split("/")[-1]
                print(website)
                if filename not in os.listdir():
                    response = requests.get(website)
                    if response.status_code == 200:
                        with open(f"{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{filename} was already downloaded")

    # The following method will check from one page to another later page
    def check_p1_p2(self, p1: int, p2: int):
        if p1 > p2:
            c = p1
            p1 = p2
            p2 = c

        for page in range(p1, p2 + 1):
            self.check_page(page)

    # The following method will check the entire archive
    def check_all(self):
        self.check_p1_p2(1, self.page_count)



if __name__ == "__main__":
    la_voix_djibouti = LaVoixDeDjibouti()
    la_voix_djibouti.check_all()