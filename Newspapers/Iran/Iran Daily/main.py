#Iran Daily pdf webscraper
#Iran Daily is a newspaper in Iran written in English



import requests,os,lxml
from bs4 import BeautifulSoup

class IranDaily:
    def __init__(self):
        self.first = 4695
        #The last number of the old archive
        self.last1 = 7246
        #The last number of the new archive
        self.last2 = self.get_last()

    #This method will find the latest number of Iran Daily
    def get_last(self)->int:
        website = "https://newspaper.irandaily.ir/archive/main"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        numbers = [int(link["href"].strip("/")) for link in soup.find_all("a",href=True) if len(link["href"])==5]
        return max(numbers)

    #This method will redirect to which method should be used to download
    #if the number is less than or equal to 7246 it will be redirected to the method that downloads the newspaper from the old archive
    #Else, it will download the newspaper from the new archive
    def download(self,number:int):
        if number <= self.last1:
            self.download_old(number)
        else:
            self.download_new(number)

    #This method will download the newspaper from the new archive
    def download_new(self,number:int):
        webpage = f"https://newspaper.irandaily.ir/{number}/1"
        main_soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
        pdfs = [link["href"] for link in main_soup.find_all("a",href=True) if "pdf" in link["href"]]
        os.makedirs(str(number))
        if len(pdfs) == 2:
            response = requests.get(url=pdfs[1])
            if response.status_code == 200:
                with open(f"{number}/{number}.pdf","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{number}/{number}.pdf was downloaded\n")
                print(f"{number}.pdf was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{number}.pdf was downloaded,it had response status code {response.status_code}\n")
                print(f"{number}.pdf was downloaded,it had response status code {response.status_code}")
        else:
            pages = [f'https://newspaper.irandaily.ir{link["href"]}' for link in main_soup.find_all("a", href=True, class_="waves-effect") if len(link["href"]) == 7 or len(link["href"]) == 8]
            for i in range(len(pages)):
                soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                for link in soup.find_all("a", href=True):
                    if "pdf" in link["href"]:
                        download_link = link["href"]

                        response = requests.get(url=download_link)

                        if response.status_code == 200:
                            with open(f"{number}/{i+1}.pdf","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{number}/{i+1}.pdf was downloaded\n")
                            print(f"{number}/{i+1}.pdf was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}")

    #This method will download the newspaper from the old archive
    def download_old(self,number:int):
        webpage = f"https://old-newspaper.irandaily.ir/?nid={number}&pid=1"
        main_soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
        pages = [link["href"] for link in main_soup.find_all('a',href=True) if "?nid" in link["href"]]
        os.makedirs(str(number))
        for i in range(len(pages)):
            website =  f"https://old-newspaper.irandaily.ir/?nid={number}&pid={i+1}"
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            for link in soup.find_all("a",href=True,title=True):
                if "نسخه" in link["title"]:
                    download_link = "https://old-newspaper.irandaily.ir"+link["href"]

                    response = requests.get(url=download_link)

                    if response.status_code == 200:
                        with open(f"{number}/{i+1}.pdf","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{number}/{i+1}.pdf was downloaded\n")
                        print(f"{number}/{i+1}.pdf was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{number}/{i+1}.pdf was downloaded,it had response status code {response.status_code}\n")
                        print(f"{number}/{i+1}.pdf was downloaded,it had response status code {response.status_code}")

    #This method will download all the newspapers from n1 till n2
    #download_n1_n2(6500,6505)
    #The following usage of the method will download:
    #6500 6501 6502 6503 6504 6505
    def download_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c
        for i in range(n1,n2+1):
            self.download(i)

    #This method will download all the old and new archive of Iran Daily
    def download_all(self):
        self.download_n1_n2(self.first,self.last2)

    #This method will download the latest copy of Iran Daily
    def download_latest(self):
        self.download(self.last2)

    # The following method will check to see if the pdf has been downloaded or not
    def check_download(self,number:int):
        if number <= self.last1:
            self.check_download_old(number)
        else:
            self.check_download_new(number)

    #This method will check the download of the newspaper from the new archive
    def check_download_new(self,number:int):
        webpage = f"https://newspaper.irandaily.ir/{number}/1"
        main_soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
        pdfs = [link["href"] for link in main_soup.find_all("a",href=True) if "pdf" in link["href"]]
        try:
            os.mkdir(str(number))
        except FileExistsError:
            pass
        if len(pdfs) == 2:
            if f"{number}.pdf" not in os.listdir(number):
                response = requests.get(url=pdfs[1])
                if response.status_code == 200:
                    with open(f"{number}/{number}.pdf","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{number}/{number}.pdf was downloaded\n")
                    print(f"{number}.pdf was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{number}.pdf was downloaded,it had response status code {response.status_code}\n")
                    print(f"{number}.pdf was downloaded,it had response status code {response.status_code}")
        else:
            pages = [f'https://newspaper.irandaily.ir{link["href"]}' for link in main_soup.find_all("a", href=True, class_="waves-effect") if len(link["href"]) == 7 or len(link["href"]) == 8]
            for i in range(len(pages)):
                if f"{i+1}.pdf" not in os.listdir(number):
                    soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                    for link in soup.find_all("a", href=True):
                        if "pdf" in link["href"]:
                            download_link = link["href"]
                            response = requests.get(url=download_link)
                            if response.status_code == 200:
                                with open(f"{number}/{i+1}.pdf","wb") as f:
                                    f.write(response.content)
                                with open("download_results.txt","a") as f:
                                    f.write(f"{number}/{i+1}.pdf was downloaded\n")
                                print(f"{number}/{i+1}.pdf was downloaded")
                            else:
                                with open("download_results.txt","a") as f:
                                    f.write(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}")

    #This method will check the download of the newspaper from the old archive
    def check_download_old(self,number:int):
        webpage = f"https://old-newspaper.irandaily.ir/?nid={number}&pid=1"
        main_soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
        pages = [link["href"] for link in main_soup.find_all('a',href=True) if "?nid" in link["href"]]
        try:
            os.mkdir(str(number))
        except FileExistsError:
            pass
        for i in range(len(pages)):
            if f"{i+1}.jpg" not in os.listdir(number):
                website =  f"https://old-newspaper.irandaily.ir/?nid={number}&pid={i+1}"
                soup = BeautifulSoup(requests.get(url=website).text,"lxml")
                for link in soup.find_all("a",href=True,title=True):
                    if "نسخه" in link["title"]:
                        download_link = "https://old-newspaper.irandaily.ir"+link["href"]
                        response = requests.get(url=download_link)
                        if response.status_code == 200:
                            with open(f"{number}/{i+1}.pdf","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{number}/{i+1}.pdf was downloaded\n")
                            print(f"{number}/{i+1}.pdf was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{number}/{i+1}.pdf was downloaded,it had response status code {response.status_code}\n")
                            print(f"{number}/{i+1}.pdf was downloaded,it had response status code {response.status_code}")

    # The following method will check from one number to another number
    def check_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c
        for i in range(n1,n2+1):
            self.check_download(i)

    # The following method will check the entire archive
    def check_all(self):
        first = self.first
        last = self.last2
        self.check_n1_n2(first,last)

if __name__ == "__main__":
    id = IranDaily()
    id.download_n1_n2(6500,6505)
