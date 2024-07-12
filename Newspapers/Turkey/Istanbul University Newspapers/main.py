#Code to download newspapers from Istanbul University
import webbrowser

import requests,os,lxml
from bs4 import BeautifulSoup




class DownloadIstanbul:

    def __init__(self):

        main_webpage = "http://nek.istanbul.edu.tr:4444/ekos/GAZETE/index.php#gazete"
        soup = BeautifulSoup(requests.get(url=main_webpage).text,"lxml")
        self.newspaper_links = [f"http://nek.istanbul.edu.tr:4444/ekos/GAZETE/{link['href']}" for link in soup.find_all("a",href=True,class_="popular-category h-40")]
        self.newspaper_names = [span.text for span in soup.find_all("span",class_="caption mb-2 d-block")]


    #This method will download all the newspapers
    def download_all(self):

        for i in range(len(self.newspaper_links)):

            newspaper_link = self.newspaper_links[i]
            newspaper_name = self.newspaper_names[i]

            os.makedirs(newspaper_name)

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
    #it will really useful for the download_newspaper methoad
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




if __name__ == "__main__":

    di = DownloadIstanbul()
    di.show_newspaper_list()
    #di.download_newspaper("")



