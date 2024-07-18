#Noor-e Khuzestan pdf webscraper
#Noor-e Khuzestan is a newspaper in Iran

import requests,lxml,os
from bs4 import BeautifulSoup



class NooreKhuzestan:
    def __init__(self):
        self.latest = self.find_latest()


    #Method to find the latest copy of Noor-e Khuzestan
    def find_latest(self)->int:
        page = "http://noordaily.ir"
        soup = BeautifulSoup(requests.get(url=page).text,"lxml")
        for link in soup.find_all("a", href=True):
            if "pid" in link["href"]:
                number = link["href"].split("=")[1].strip('&pid')
                return number

    #This method will download ith numbered newspapers pages
    def download(self,i):
        number = str(i)
        page = f"http://noordaily.ir/?nid={number}&pid=1&type=0"
        soup = BeautifulSoup(requests.get(url=page).text, "lxml")
        links = list(set([anchor["href"] for anchor in soup.find_all("a", href=True) if "pid" in anchor["href"]]))
        links.sort()
        links = [f"http://noordaily.ir{link}" for link in links]
        print(links)
        try:
            os.makedirs(number)
        except FileExistsError:
            pass

        for i in range(len(links)):
            link = links[i]
            page_number = i + 1
            filename = f"{number}_{page_number}.jpg"
            content = requests.get(url=link)
            new_soup = BeautifulSoup(content.text, 'lxml')
            images = new_soup.find_all("img", src=True)
            image = [f'http://noordaily.ir{image["src"]}' for image in new_soup.find_all("img", src=True) if "/content/newspaper/Version" in image["src"]][0]
            print(image)

            response = requests.get(url=image)
            if response.status_code == 200:
                with open(f"{number}/{filename}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{number}/{filename} was downloaded\n")
                print(f"{number}/{filename} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{number}/{filename} was not downloaded {response.status_code}\n")
                print(f"{number}/{filename} was not downloaded {response.status_code}")

    #The following method will download all the pdfs
    def download_all(self):
        for i in range(5706,self.latest+1):
            self.download(i)

    #This method will download a specifically specified number pdf
    def download_number(self,number:int):
        self.download(number)

    #This method will download all the newspapers from n1 till n2
    #For example
    #nk = NooreKhuzestan()
    #nk.download_n1_n2(6500, 6502)
    #will download Noor-e Khuzestan numbered 6500 6501 6502
    def download_n1_n2(self,n1,n2):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c
        for i in range(n1,n2+1):
            self.download(i)

if __name__ == "__main__":
    nk = NooreKhuzestan()
    nk.download_n1_n2(6500,6502)