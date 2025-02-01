#Juraj Šižgorić City Library
import os

import requests,lxml
from bs4 import BeautifulSoup

class JurajLibrary:
    def __init__(self):
        self.site = 'http://212.92.192.228/'
        self.links = []
        self.category_data = {}
        self.link_data = {}
        self.gather_data()

    def gather_data(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        links = [f"{n['href']}" for n in soup.find_all('a',href=True) if '.pdf' in n['href']]
        for link in links:
            category = link.split("/")[1]
            name = link.split("/")[-1].split("_1")[0]
            if category not in self.category_data:
                self.category_data[category] = [name]
            else:
                if name not in self.category_data[category]:
                    self.category_data[category].append(name)
            if name not in self.link_data:
                self.link_data[name] = [f"http://212.92.192.228/{link}"]
            else:
                self.link_data[name].append(f"http://212.92.192.228/{link}")
        self.links = links

    # The following method will print all the categories on the website
    def print_categories(self):
        for category in self.category_data:
            print(category)

    # The following method will print all the title of a particular category
    def print_category_titles(self,category:str):
        if category in self.category_data:
            for title in self.category_data[category]:
                print(title)

    # The following method will print all the links for a particular title
    def print_title_links(self,title:str):
        if title in self.link_data:
            for link in self.link_data[title]:
                print(link)

    # The following method will download a specific title
    def download_title(self,title:str):
        if title in self.link_data:
            for c in self.category_data[c]:
                if title in c:
                    os.makedirs(f"{c}/{title}")
                    break
            for link in self.link_data[title]:
                filename = link.split("/")[-1]
                response = requests.get(link)
                if response.status_code == 200:
                    with open(f"{c}/{title}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt",'a') as f:
                        f.write(f"{c}/{title}/{filename} was downloaded.\n")
                    print(f"{c}/{title}/{filename} was downloaded.")
                else:
                    with open("download_results.txt",'a') as f:
                        f.write(f"{c}/{title}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{c}/{title}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download a specific category
    def download_category(self,category:str):
        if category in self.category_data:
            for title in self.category_data[category]:
                self.download_title(title)

    # The following method will download all
    def download_all(self):
        for category in self.category_data:
            self.download_category(category)

    # The following method will check if all the pdfs for a title were downloaded or not
    def check_title(self,title:str):
        if title in self.link_data:
            for c in self.category_data:
                if title in self.category_data[c]:
                    os.makedirs(f"{c}/{title}",exist_ok=True)
                    break
            for link in self.link_data[title]:
                filename = link.split("/")[-1]
                if filename not in os.listdir(f"{c}/{title}"):
                    response = requests.get(link)
                    if response.status_code == 200:
                        with open(f"{c}/{title}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open("download_results.txt", 'a') as f:
                            f.write(f"{c}/{title}/{filename} was downloaded.\n")
                        print(f"{c}/{title}/{filename} was downloaded.")
                    else:
                        with open("download_results.txt", 'a') as f:
                            f.write( f"{c}/{title}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{c}/{title}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will check a specific category
    def check_category(self,category:str):
        if category in self.category_data:
            for title in self.category_data[category]:
                self.check_title(title)

    # The following method will check the entire archive
    def check_all(self):
        for category in self.category_data:
            self.check_category(category)



if __name__ == "__main__":
    jl = JurajLibrary()
    jl.check_all()