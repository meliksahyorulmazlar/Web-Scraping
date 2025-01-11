#Webscraper to get/download pdfs of webaram.com
import requests,os,lxml
from bs4 import BeautifulSoup


class WebAram:
    def __init__(self):
        self.main_page = "https://webaram.com/biblio/presse"
        self.soup = BeautifulSoup(requests.get(url=self.main_page).text,"lxml")
        self.newspaper_links = sorted(list(set([link['href'] for link in self.soup.find_all("a",href=True) if "https://webaram.com/biblio/presse/" in link["href"]])))
        self.newspaper_dictionary = {}
        self.get_names()

    # The following method will get the names of all the newspapers
    def get_names(self):
        for link in self.newspaper_links:
            soup = BeautifulSoup(requests.get(url=link).text,"lxml")
            name = soup.find("h1").text
            self.newspaper_dictionary[name] = link

    #The following method will print the names of all the newspapers
    def print_names(self):
        for key in self.newspaper_dictionary:
            print(key)

    #The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            link = self.newspaper_dictionary[newspaper]
            date_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
            pdf_links = [link["href"] for link in date_soup.find_all("a", href=True, target=True) if "liseuse" not in link["href"] and link["target"] == '_blank' and "pdf" in link["href"]]
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            for pdf in pdf_links:
                response = requests.get(url=pdf)
                filename = pdf.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{newspaper}/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will download all the newspapers
    def download_all(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    # The following method will check if all the pdfs of a specific newspaper have been downloaded or not
    def check_newspaper(self,newspaper):
        if newspaper in self.newspaper_dictionary:
            link = self.newspaper_dictionary[newspaper]
            date_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
            pdf_links = [link["href"] for link in date_soup.find_all("a", href=True, target=True) if
                         "liseuse" not in link["href"] and link["target"] == '_blank' and "pdf" in link["href"]]
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            for pdf in pdf_links:
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(newspaper):
                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f"{newspaper}/{filename}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{filename} was downloaded\n")
                        print(f"{filename} was downloaded")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

if __name__ == "__main__":
    wa = WebAram()
    wa.download_all()
