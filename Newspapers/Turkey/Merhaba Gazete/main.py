#Merhaba Gazete Pdf webscraper
#Merhaba is a newspaper in Konya,Turkey



import requests,os,lxml
from bs4 import BeautifulSoup


class MerhabaGazete:
    def __init__(self):
        self.first_page = 1
        self.last_page = self.find_last()


    #This will find the last page of the archive
    def find_last(self)->int:
        #When I last checked the archive had 79 pages
        count = 79
        found = False
        while not found:
            webpage = f"https://www.merhabahaber.com/egazete/merhaba-gazetesi-1-p{count}.htm"
            soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
            pages = [int(link.text) for link in soup.find_all("a",href=True,rel=True) if len(link.text)>0]
            greatest = max(pages)
            if count > greatest:
                found = True
            else:
                print(greatest)
                count = greatest
        return count

    #This method will find the newspapers of the page and return a list of the newspapers
    def find_newspapers(self,number:int)->list:
        webpage = f"https://www.merhabahaber.com/egazete/merhaba-gazetesi-1-p{number}.htm"
        soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
        links = [(f'https://www.merhabahaber.com{link["href"]}',link.text) for link in soup.find_all("a",href=True) if "/egazete/merhaba-gazetesi/" in link["href"]]
        return links[::-1]

    #This will download the entire page
    def download_page(self,number:int):
        links = self.find_newspapers(number)
        print(links)
        for link in links:
            self.download_link(link)


    #This will download a link and save it as its number-date
    #3820-18.07.2024
    #3820 is the number,18.07.2024 is the date
    def download_link(self,link_date:tuple):
        download_link = link_date[0]
        date = link_date[1]


        soup = BeautifulSoup(requests.get(url=download_link).text,"lxml")
        pages = [(image["alt"],image["src"]) for image in soup.find_all("img",src=True,alt=True) if "Sayfa" in image["alt"]]
        pages.pop()

        for i in range(len(pages)):
            download_link = pages[i][1].split("/")
            number = download_link[-2]
            changed = download_link[-1].replace("_s","")
            download_link[-1] = changed
            download_link = "/".join(download_link)

            response = requests.get(url=download_link)

            directory1 = f"{number}-{date}"
            try:
                os.makedirs(directory1)
            except FileExistsError:
                pass

            if response.status_code == 200:
                with open(f"{directory1}/{changed}","wb") as f:
                    f.write(response.content)

                with open("download_results.txt","a") as f:
                    f.write(f"{directory1}/{changed} was downloaded\n")
                print(f"{directory1}/{changed} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{directory1}/{changed} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{directory1}/{changed} was not downloaded,it had response status code {response.status_code}")

    #This method will download all the pages from n1 till
    #download_n1_n2(1,2)
    #will download all of pages 1 and 2 of Merhaba Gazete
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n2
            n2 = n1
            n1 = c

        for i in range(n2,n1-1,-1):
            self.download_page(i)

    #This method will download all the newspapers
    def download_all(self):
        self.download_n1_n2(self.first_page,self.last_page)

    #This method will download the latest copy of Merhaba Gazete
    def download_latest(self):
        links = self.find_newspapers(1)
        link = links[-1]
        self.download_link(link)

if __name__ == "__main__":
    mg = MerhabaGazete()
    mg.download_latest()

