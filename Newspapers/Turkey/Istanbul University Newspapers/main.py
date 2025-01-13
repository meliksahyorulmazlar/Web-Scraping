#Code to download newspapers from Istanbul University

import requests,os,lxml
from bs4 import BeautifulSoup

class IstanbulUniversity:
    def __init__(self):
        main_webpage = 'https://nek.istanbul.edu.tr/ekos/GAZETE/index.php#gazete'
        print(requests.get(main_webpage).status_code)
        soup = BeautifulSoup(requests.get(url=main_webpage).text,"lxml")
        self.newspaper_links = [f"http://nek.istanbul.edu.tr:4444/ekos/GAZETE/{link['href']}" for link in soup.find_all("a",href=True,class_="popular-category h-40")]
        self.newspaper_names = [span.text for span in soup.find_all("span",class_="caption mb-2 d-block")]
        print(self.newspaper_names)
        print(self.newspaper_links)
        print(len(self.newspaper_names))
        print(len(self.newspaper_links))
        exit()

    #This method will download all the newspapers
    def download_all(self):
        for i in range(len(self.newspaper_links)):
            newspaper_link = self.newspaper_links[i]
            newspaper_name = self.newspaper_names[i]

            try:
                os.mkdir(newspaper_name)
            except FileExistsError:
                pass

            newspaper_soup = BeautifulSoup(requests.get(url=newspaper_link).text,"lxml")
            newspapers = [anchor_tag["href"].replace(" ","%20") for anchor_tag in newspaper_soup.find_all("a") if "pdf" in anchor_tag["href"]]

            for newspaper in newspapers:

                response = requests.get(url=newspaper)
                filename = newspaper.replace("%20"," ").split("/")[-1]

                if response.status_code == 200:
                    with open(f"{newspaper_name}/{filename}","wb") as f:
                        f.write(response.content)
                    print(f"{filename} was downloaded")
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded\n")
                else:
                    print(f"{newspaper_name} had response status code {response.status_code}")
                    with open("download_results.txt","a") as f:
                        f.write(f"{newspaper_name} had response status code {response.status_code}")

    #You can use to find this to get the names of the newspapers
    #it will really useful for the download_newspaper method
    #You can just the copy paste the newspaper you want to download for the newspaper_name input
    def show_newspaper_list(self):
        print(self.newspaper_names)

    #This method downloads all of a newspaper
    def download_newspaper(self,newspaper_name:str):
        if newspaper_name in self.newspaper_names:
            index = self.newspaper_names.index(newspaper_name)
            newspaper_link = self.newspaper_links[index]


            os.makedirs(newspaper_name)

            newspaper_soup = BeautifulSoup(requests.get(url=newspaper_link).text, "lxml")
            newspapers = [anchor_tag["href"].replace(" ", "%20") for anchor_tag in newspaper_soup.find_all("a") if "pdf" in anchor_tag["href"]]

            for newspaper in newspapers:

                response = requests.get(url=newspaper)
                filename = newspaper.replace("%20", " ").split("/")[-1]

                if response.status_code == 200:
                    with open(f"{newspaper_name}/{filename}", "wb") as f:
                        f.write(response.content)
                    print(f"{filename} was downloaded")
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was downloaded\n")
                else:
                    print(f"{newspaper_name} had response status code {response.status_code}")
                    with open("download_results.txt", "a") as f:
                        f.write(f"{newspaper_name} had response status code {response.status_code}")
        else:
            print(f"Newspaper not found")

    #The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspaper_names:
            self.download_newspaper(newspaper)

    # The following method will download the newspapers that have not been downloaded
    def check_newspaper(self,newspaper_name:str):
        if newspaper_name in self.newspaper_names:
            index = self.newspaper_names.index(newspaper_name)
            newspaper_link = self.newspaper_links[index]

            try:
                os.mkdir(newspaper_name)
            except FileExistsError:
                pass

            newspaper_soup = BeautifulSoup(requests.get(url=newspaper_link).text, "lxml")
            newspapers = [anchor_tag["href"].replace(" ", "%20") for anchor_tag in newspaper_soup.find_all("a") if "pdf" in anchor_tag["href"]]

            for newspaper in newspapers:
                filename = newspaper.replace("%20", " ").split("/")[-1]
                if filename not in os.listdir(newspaper_name):
                    response = requests.get(url=newspaper)

                    if response.status_code == 200:
                        with open(f"{newspaper_name}/{filename}", "wb") as f:
                            f.write(response.content)
                        print(f"{filename} was downloaded")
                        with open("download_results.txt", "a") as f:
                            f.write(f"{filename} was downloaded\n")
                    else:
                        print(f"{newspaper_name} had response status code {response.status_code}")
                        with open("download_results.txt", "a") as f:
                            f.write(f"{newspaper_name} had response status code {response.status_code}")
        else:
            print(f"Newspaper not found")

    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_names:
            self.check_newspaper(newspaper)

if __name__ == "__main__":
    iu = IstanbulUniversity()
    iu.show_newspaper_list()
    iu.check_newspapers()
