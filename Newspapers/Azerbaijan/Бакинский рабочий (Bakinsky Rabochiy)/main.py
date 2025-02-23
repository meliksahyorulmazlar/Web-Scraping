#Бакинский рабочий a newspaper from Azerbaijan
#Bakinsky Rabochiy meaning Baku Worker
import os

import requests,lxml,selenium,time
from bs4 import BeautifulSoup
from selenium import webdriver

class BakinskyRabochiy:
    def __init__(self):
        self.main_page = "https://br.az/newspaper/?page=1"
        self.number_pages = 0

    #This method will find how many pages there are on the archive
    def find_count(self):
        #When I last checked there were 216 pages on the archive
        count = 216
        all_found = False
        while not all_found:
            page = f"https://br.az/newspaper/?page={count}"
            print(page)

            soup = BeautifulSoup(requests.get(url=page).text,"lxml")
            pages = [link['href'] for link in soup.find_all("a",href=True) if "page=" in link["href"]]
            numbers = [int(page.split("=")[1]) for page in pages]
            print(numbers)
            if max(numbers) < count:
                all_found = True
            else:
                count = max(numbers)
                print(count)
        return count

    #Method to download pdfs
    def download_pdf(self,download_link:str):
        response = requests.get(url=download_link)
        filename = download_link.split("/")[-1]

        if response.status_code == 200:
            with open(f"{filename}","wb") as f:
                f.write(response.content)
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was downloaded\n")
            print(f"{filename} was downloaded")
        else:
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
            print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    #This will download the latest newspaper
    def download_latest(self):
        page = f"https://br.az/newspaper/?page=1"
        soup = BeautifulSoup(requests.get(url=page).text,"lxml")
        pdf_link = [f'https://br.az{link["href"]}' for link in soup.find_all("a",href=True) if "pdf" in link["href"]][0]
        self.download_pdf(download_link=pdf_link)

    #As of the 16th July 2024, there are 216 pages on the archive
    #If you enter a number between 1 and 214 inclusive,
    #It will download that page
    #The following example will download the 5th page
    #br.download_page(page_number=5)
    def download_page(self,page_number:int):
        page = f"https://br.az/newspaper/?page={page_number}"
        soup = BeautifulSoup(requests.get(url=page).text, "lxml")
        pdf_links = [f'https://br.az{link["href"]}' for link in soup.find_all("a", href=True) if "pdf" in link["href"]]
        for link in pdf_links:
            self.download_pdf(download_link=link)

    # The following method will download from the n1th page till the n2nd page
    def download_page1_page2(self,page1:int,page2:int):
        if page1 > page2:
            c = page1
            page1 = page2
            page2 = c

        for i in range(page1,page2+1):
            self.download_page(i)

    #This will download the entire archive
    def download_all(self):
        self.download_page1_page2(1,self.number_pages)

    # The following method will check if a pdf has been downloaded or not
    def check_pdf(self,download_link:str):
        filename = download_link.split("/")[-1]
        if filename not in os.listdir():
            response = requests.get(url=download_link)
            if response.status_code == 200:
                with open(f"{filename}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will check a particular to see if its pdfs got downloaded or not
    def check_page(self,page_number:int):
        page = f"https://br.az/newspaper/?page={page_number}"
        soup = BeautifulSoup(requests.get(url=page).text, "lxml")
        pdf_links = [f'https://br.az{link["href"]}' for link in soup.find_all("a", href=True) if "pdf" in link["href"]]
        for link in pdf_links:
            self.check_pdf(download_link=link)

    # This method will check all the pages to see if the files have been downloaded or not
    def check_page1_page2(self,page1:int,page2:int):
        if page1 > page2:
            c = page1
            page1 = page2
            page2 = c

        for i in range(page1,page2+1):
            self.check_page(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_page1_page2(1,self.number_pages)


if __name__ == "__main__":
    br = BakinskyRabochiy()
    br.download_latest()
