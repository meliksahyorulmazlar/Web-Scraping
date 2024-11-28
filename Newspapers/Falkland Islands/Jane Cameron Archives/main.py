# James Cameron Archive
import os

import requests,lxml
from bs4 import BeautifulSoup



class JamesCameronArchives:
    def __init__(self):
        self.main_page = "https://www.nationalarchives.gov.fk"
        self.dictionary = {}
        self.categorize()

    # Categorize the urls
    def categorize(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text, 'lxml')
        lis = [li for li in soup.find_all("li", class_='sp-menu-item')]
        anchor_tags = [li.find_next("a") for li in lis]
        result = [(anchor_tag.text,anchor_tag["href"]) for anchor_tag in anchor_tags if 'online-collections/' in anchor_tag['href']]

        new = []
        for r in result:
            if r not in new:
                new.append(r)
        self.dictionary = {}
        c = 0
        for r in new:
            item = r[1]
            list_form:list = item.split("/")
            list_form.pop(0)
            list_form.pop(0)
            key = list_form[0]
            value = "/".join(list_form[1:])

            c+= 1
            if key in self.dictionary:
                self.dictionary[key].append(value)
            elif key not in self.dictionary:
                if value:
                    self.dictionary[key] = [value]
                else:
                    self.dictionary[key] = []

    # The following method will print all the categories that can be downloaded
    def print_categories(self):
        for key in self.dictionary:
            print(key)

    # The following method will download a specific given category
    def download_category(self,category:str):
        if category in self.dictionary:
            length = len(self.dictionary[category])
            if length == 0:

                os.mkdir(category)
                website = f"https://www.nationalarchives.gov.fk/online-collections/{category}"
                soup = BeautifulSoup(requests.get(url=website).text,'lxml')
                pdfs = [f'https://www.nationalarchives.gov.fk{link['href']}' for link in soup.find_all("a",href=True) if "jdownloads" in link['href']]

                for p in pdfs:
                    split_form = p.split("/")
                    filename = split_form[-1].replace("%20"," ")

                    response = requests.get(url=p)
                    if response.status_code == 200:
                        with open(f"{category}/{filename}","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{category}/{filename} was downloaded\n")
                        print(f"{category}/{filename} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{category}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{category}/{filename} was not downloaded,it had response status code {response.status_code}")
            else:
                websites = []
                os.mkdir(category)
                for item in self.dictionary[category]:
                    website = f"https://www.nationalarchives.gov.fk/online-collections/{category}/{item}"
                    websites.append(website)
                    items = item.split("/")
                    directory = ""
                    for i in range(len(items)):
                        part1 = f"{category}/"
                        part2 = "/".join(items[0:i+1])
                        directory = part1 + part2
                        try:
                            os.mkdir(directory)
                        except FileExistsError:
                            pass
                    soup = BeautifulSoup(requests.get(url=website).text,'lxml')
                    pdfs = [f'https://www.nationalarchives.gov.fk{link['href']}' for link in soup.find_all("a", href=True) if "jdownloads" in link['href']]

                    for p in pdfs:
                        split_form = p.split("/")
                        filename = split_form[-1].replace("%20", " ")

                        response = requests.get(url=p)
                        if response.status_code == 200:
                            with open(f"{directory}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{directory}/{filename} was downloaded\n")
                            print(f"{category}/{filename} was downloaded")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"{directory}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{directory}/{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will download all the categories
    def download_categories(self):
        for category in self.dictionary:
            self.download_category(category)

    # This method will check if there are any missing files to be downloaded for a particular category
    def check_category(self,category:str):
        try:
            items = os.listdir(category)
        except FileNotFoundError:
            self.download_category(category)
        else:
            length = len(self.dictionary[category])
            if length == 0:
                website = f"https://www.nationalarchives.gov.fk/online-collections/{category}"
                soup = BeautifulSoup(requests.get(url=website).text,'lxml')
                pdfs = [f'https://www.nationalarchives.gov.fk{link['href']}' for link in soup.find_all("a",href=True) if "jdownloads" in link['href']]

                for p in pdfs:
                    split_form = p.split("/")
                    filename = split_form[-1].replace("%20"," ")

                    if filename not in items:
                        response = requests.get(url=p)
                        if response.status_code == 200:
                            with open(f"{category}/{filename}","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{category}/{filename} was downloaded\n")
                            print(f"{category}/{filename} was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{category}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{category}/{filename} was not downloaded,it had response status code {response.status_code}")
            else:
                websites = []
                try:
                    os.mkdir(category)
                except FileExistsError:
                    pass

                for item in self.dictionary[category]:
                    website = f"https://www.nationalarchives.gov.fk/online-collections/{category}/{item}"
                    websites.append(website)
                    items = item.split("/")
                    directory = ""
                    for i in range(len(items)):
                        part1 = f"{category}/"
                        part2 = "/".join(items[0:i+1])
                        directory = part1 + part2
                        try:
                            os.mkdir(directory)
                        except FileExistsError:
                            pass
                    soup = BeautifulSoup(requests.get(url=website).text,'lxml')
                    pdfs = [f'https://www.nationalarchives.gov.fk{link['href']}' for link in soup.find_all("a", href=True) if "jdownloads" in link['href']]
                    items = os.listdir(directory)
                    for p in pdfs:
                        split_form = p.split("/")

                        filename = split_form[-1].replace("%20", " ")

                        if filename not in items:
                            response = requests.get(url=p)
                            if response.status_code == 200:
                                with open(f"{directory}/{filename}", "wb") as f:
                                    f.write(response.content)
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{directory}/{filename} was downloaded\n")
                                print(f"{category}/{filename} was downloaded")
                            else:
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{directory}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{directory}/{filename} was not downloaded,it had response status code {response.status_code}")


    # This method will check if there are any missing files to be downloaded for all the categories
    def check_categories(self):
        for category in self.dictionary:
            self.download_category(category)




if __name__ == "__main__":
    jca = JamesCameronArchives()
    jca.download_categories()

