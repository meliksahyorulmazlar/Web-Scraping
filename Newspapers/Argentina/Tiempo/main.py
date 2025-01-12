#Tiempo front page webscraper
#Tiempo is a newspaper in Argentina
import os

import requests,lxml
from bs4 import BeautifulSoup


class Tiempo:
    def __init__(self):
        self.page_count = self.find_count()

    #This method will find the number of pages there are on the archive
    def find_count(self)->int:
        website = "https://www.tiempoar.com.ar/ediciones-impresas"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        page_numbers = [int(link.text) for link in soup.find_all("a",href=True,class_="page-numbers") if len(link.text)>0]
        return max(page_numbers)

    #This method will download the entire archive
    def download_all(self):
        for i in range(1,self.page_count+1):
            self.download_page(i)

    def download_page(self,number:int):
        if 1 <= number <= self.page_count:
            i = number
            page = f"https://www.tiempoar.com.ar/ediciones-impresas/page/{i}/"
            soup = BeautifulSoup(requests.get(url=page).text, "lxml")
            pages = []
            for link in soup.find_all("a", href=True):
                if "ta_ed_impresa" in link["href"] or "ediciones-impresas/2" in link["href"]:
                    if link["href"] not in pages:
                        pages.append(link["href"])

            print(pages)
            for page in pages:
                soup = BeautifulSoup(requests.get(url=page).text,"lxml")
                image_tags = soup.find_all("img")
                date = page.split("/")[-2]
                print(date)
                try:
                    image_tag = [image_tag["src"] for image_tag in image_tags if "https://www.tiempoar.com.ar/wp-content/uploads/" in image_tag["src"] and ".jpg" in image_tag['src']][0]
                except IndexError:
                    with open("download_results.txt", 'a') as file:
                        file.write(f"{i} {date} had no image\n")
                    print(f"{i} {date} had no image")
                else:
                    image = requests.get(image_tag).content
                    with open(f"{date}.jpg", 'wb') as file:
                        file.write(image)
                    print(f"{i} {date} was downloaded")
                    with open("download_results.txt", 'a') as file:
                        file.write(f"{i} {date} was downloaded\n")

    # This method will download the first page
    def download_first_page(self):
       self.download_page(1)

    # The following method will check a particular page number
    def check_page(self,number:int):
        if 1 <= number <= self.page_count:
            i = number
            page = f"https://www.tiempoar.com.ar/ediciones-impresas/page/{i}/"
            soup = BeautifulSoup(requests.get(url=page).text, "lxml")
            pages = []
            for link in soup.find_all("a", href=True):
                if "ta_ed_impresa" in link["href"] or "ediciones-impresas/2" in link["href"]:
                    if link["href"] not in pages:
                        pages.append(link["href"])
            print(pages)
            for page in pages:
                soup = BeautifulSoup(requests.get(url=page).text,"lxml")
                image_tags = soup.find_all("img")
                date = page.split("/")[-2]
                print(date)
                try:
                    image_tag = [image_tag["src"] for image_tag in image_tags if "https://www.tiempoar.com.ar/wp-content/uploads/" in image_tag["src"] and ".jpg" in image_tag['src']][0]
                except IndexError:
                    with open("download_results.txt", 'a') as file:
                        file.write(f"{i} {date} had no image\n")
                    print(f"{i} {date} had no image")
                else:
                    if f"{date}.jpg" not in os.listdir():
                        image = requests.get(image_tag).content
                        with open(f"{date}.jpg", 'wb') as file:
                            file.write(image)
                        print(f"{i} {date} was downloaded")
                        with open("download_results.txt", 'a') as file:
                            file.write(f"{i} {date} was downloaded\n")

    # The following method will check from one particular page number to another page number
    def check_page1_page2(self,page1:int,page2:int):
        if page1 > page2:
            c = page1
            page1 = page2
            page2 = c

        for page in range(page1,page2):
            self.check_page(page)

    # The following method will check all the page numbers
    def check_all(self):
        self.check_page1_page2(1,self.page_count)
        
if __name__ == "__main__":
    tiempo = Tiempo()
    tiempo.download_latest()
