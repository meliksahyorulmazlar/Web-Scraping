#Iran Newspaper pdf webscraper
#Iran (ایران) Newspaper is a famous newspaper in Iran
import webbrowser

import requests,os,lxml
from bs4 import BeautifulSoup



class IranNewspaper:
    def __init__(self):
        #This is the earliest number on the archive
        self.first = 5555
        #This is the last number on the old archive
        self.latest1 = 8105
        #This is the last number on the current/new archive
        self.latest2 = self.find_latest_newspaper()

        #Special Iran Newspaper Magazine
        self.special_first = 130
        self.special_last = self.find_latest_magazine()

    # This method will find the latest number of Iran Newspaper
    def find_latest_newspaper(self)->int:
        website = "https://irannewspaper.ir/archive/main"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        numbers = [int(link["href"].strip("/")) for link in soup.find_all("a", href=True) if len(link["href"]) == 5]
        return max(numbers)

    #This method will find the latest number of Iran Newspaper magazine
    def find_latest_magazine(self)->int:
        website = "https://irannewspaper.ir/archive/specials"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        numbers = [int(link["href"].strip("/sp-")) for link in soup.find_all("a", href=True) if len(link["href"]) == 7]
        return max(numbers)


    #This method will redirect to which method should be used to download
    #if the number is less than or equal to 8105 it will be redirected to the method that downloads the newspaper from the old archive
    #Else, it will download the newspaper from the new archive
    def download(self,number:int):
        if number <= self.latest1:
            self.download_old(number)
        else:
            self.download_new(number)

    #This method will download the newspaper from the old archive
    def download_old(self,number:int):
        os.makedirs(str(number))
        webpage = f"https://old.irannewspaper.ir/?nid={number}&pid=1&type=0"
        main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
        pages = [link["href"] for link in main_soup.find_all('a', href=True) if "?nid" in link["href"]]
        links = [div.find("a")["href"] for div in main_soup.find_all("div",class_="photo")]
        links = [f"https://old.irannewspaper.ir{link}" for link in links]
        for i in range(len(links)):
            response = requests.get(url=links[i])

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

    def download_new(self,number:int):
        webpage = f"https://irannewspaper.ir/{number}/2"
        main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
        pdfs = [link["href"] for link in main_soup.find_all("a", href=True) if "pdf" in link["href"]]
        os.makedirs(str(number))
        if len(pdfs) == 2:
            response = requests.get(url=pdfs[1])
            if response.status_code == 200:
                with open(f"{number}/{number}.pdf", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{number}/{number}.pdf was downloaded\n")
                print(f"{number}.pdf was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{number}.pdf was downloaded,it had response status code {response.status_code}\n")
                print(f"{number}.pdf was downloaded,it had response status code {response.status_code}")
        else:
            pages = [f'https://irannewspaper.ir/{link["href"]}' for link in main_soup.find_all("a", href=True, class_="waves-effect") if len(link["href"]) == 7 or len(link["href"]) == 8]
            print(pages)
            for i in range(len(pages)):
                soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                for link in soup.find_all("a", href=True):
                    if "pdf" in link["href"]:
                        download_link = link["href"]

                        response = requests.get(url=download_link)

                        if response.status_code == 200:
                            with open(f"{number}/{i + 1}.pdf", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{number}/{i + 1}.pdf was downloaded\n")
                            print(f"{number}/{i + 1}.pdf was downloaded")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"{number}/{i + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{number}/{i+1}.pdf was not downloaded,it had response status code {response.status_code}")

    #This method will download all the newspapers from n1 to n2
    #download_n1_n2(8500,8505)
    #will download 8500,8501,8502,8503,8504,8505
    def download_n1_n2(self,n1:int,n2:int):
        if n1 >n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download(i)

    #This method will download all the newspapers on the old and new archive
    def download_all(self):
        for i in range(self.first,self.latest2+1):
            self.download(i)

    #This method will download the latest copy of Iran Newspaper
    def download_latest(self):
        self.download_new(self.latest2)


    #This method will download a magazine given its number
    def download_magazine(self,number:int):
        webpage = f"https://irannewspaper.ir/sp-{number}"
        main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
        pdfs = [link["href"] for link in main_soup.find_all("a", href=True) if "pdf" in link["href"]]
        os.makedirs(f"sp-{number}")
        if len(pdfs) == 2:
            response = requests.get(url=pdfs[1])
            if response.status_code == 200:
                with open(f"sp-{number}/sp-{number}.pdf", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"sp-{number}/sp-{number}.pdf was downloaded\n")
                print(f"sp-{number}.pdf was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"sp-{number}.pdf was not downloaded,it had response status code {response.status_code}\n")
                print(f"sp-{number}.pdf was not downloaded,it had response status code {response.status_code}")
        else:
            pages = [f'https://irannewspaper.ir/{link["href"]}' for link in main_soup.find_all("a", href=True, class_="waves-effect") if len(link["href"]) == 9 or len(link["href"]) == 10 or len(link['href']) == 11]
            print(pages)
            for i in range(len(pages)):
                soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                for link in soup.find_all("a", href=True):
                    if "pdf" in link["href"]:
                        download_link = link["href"]

                        response = requests.get(url=download_link)

                        if response.status_code == 200:
                            with open(f"sp-{number}/sp-{i + 1}.pdf", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"sp-{number}/sp-{i + 1}.pdf was downloaded\n")
                            print(f"sp-{number}/sp-{i + 1}.pdf was downloaded")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"sp-{number}/sp-{i + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                            print(f"sp-{number}/sp-{i + 1}.pdf was not downloaded,it had response status code {response.status_code}")

    # This method will download all the magazine from n1 to n2
    # download_n1_n2_magazines(300,305)
    # will download 300,301,302,303,304,305
    def download_n1_n2_magazines(self,n1:int,n2:int):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c

        for i in range(n1,n2+1):
            self.download_magazine(i)

    #This method will download all the magazines
    def download_all_magazines(self):
        self.download_n1_n2_magazines(self.special_first,self.special_last+1)


    #This method will download the latest magazines
    def download_latest_magazine(self):
        self.download_magazine(self.special_last)

    # The following method will check if the images for a particular number got downloaded or not
    def check_download(self,number:int):
        if number <= self.latest1:
            self.check_download_old(number)
        else:
            self.check_download_new(number)

    # The following method will check the old archive to see if all the images got downloaded or not
    def check_download_old(self,number:int):
        try:
            os.mkdir(str(number))
        except FileExistsError:
            pass
        webpage = f"https://old.irannewspaper.ir/?nid={number}&pid=1&type=0"
        main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
        pages = [link["href"] for link in main_soup.find_all('a', href=True) if "?nid" in link["href"]]
        links = [div.find("a")["href"] for div in main_soup.find_all("div", class_="photo")]
        links = [f"https://old.irannewspaper.ir{link}" for link in links]
        for i in range(len(links)):
            if f"{i+1}.pdf" not in os.listdir(str(number)):
                response = requests.get(url=links[i])
                if response.status_code == 200:
                    with open(f"{number}/{i + 1}.pdf", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{i + 1}.pdf was downloaded\n")
                    print(f"{number}/{i + 1}.pdf was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(
                            f"{number}/{i + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{number}/{i + 1}.pdf was not downloaded,it had response status code {response.status_code}")

    # The following method will check the new archive to see if all the images got downloaded or not
    def check_download_new(self,number:int):
        webpage = f"https://irannewspaper.ir/{number}/2"
        main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
        pdfs = [link["href"] for link in main_soup.find_all("a", href=True) if "pdf" in link["href"]]
        try:
            os.mkdir(str(number))
        except FileExistsError:
            pass
        if len(pdfs) == 2:
            if f"{number}.pdf" not in os.listdir(f"{number}"):
                response = requests.get(url=pdfs[1])
                if response.status_code == 200:
                    with open(f"{number}/{number}.pdf", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}/{number}.pdf was downloaded\n")
                    print(f"{number}.pdf was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{number}.pdf was downloaded,it had response status code {response.status_code}\n")
                    print(f"{number}.pdf was downloaded,it had response status code {response.status_code}")
        else:
            pages = [f'https://irannewspaper.ir/{link["href"]}' for link in
                     main_soup.find_all("a", href=True, class_="waves-effect") if
                     len(link["href"]) == 7 or len(link["href"]) == 8]
            print(pages)
            for i in range(len(pages)):
                if f"{i+1}.pdf" not in os.listdir(str(number)):
                    soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                    for link in soup.find_all("a", href=True):
                        if "pdf" in link["href"]:
                            download_link = link["href"]
                            response = requests.get(url=download_link)
                            if response.status_code == 200:
                                with open(f"{number}/{i + 1}.pdf", "wb") as f:
                                    f.write(response.content)
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{number}/{i + 1}.pdf was downloaded\n")
                                print(f"{number}/{i + 1}.pdf was downloaded")
                            else:
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{number}/{i + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{number}/{i + 1}.pdf was not downloaded,it had response status code {response.status_code}")

    #This method will check all the newspapers from n1 to n2
    def check_n1_n2(self,n1:int,n2:int):
        if n1 >n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download(i)

    #This method will download all the newspapers on the old and new archive
    def check_all(self):
        self.check_n1_n2(self.first,self.latest2)

    #This method will check a magazine given its number
    def check_magazine(self,number:int):
        if self.special_first <= number <= self.special_last:
            webpage = f"https://irannewspaper.ir/sp-{number}"
            main_soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
            pdfs = [link["href"] for link in main_soup.find_all("a", href=True) if "pdf" in link["href"]]
            try:
                os.mkdir(f"sp-{number}")
            except FileExistsError:
                pass
            if len(pdfs) == 2:
                if f"sp-{number}.pdf" not in os.listdir(f"sp-{number}"):
                    response = requests.get(url=pdfs[1])
                    if response.status_code == 200:
                        with open(f"sp-{number}/sp-{number}.pdf", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"sp-{number}/sp-{number}.pdf was downloaded\n")
                        print(f"sp-{number}.pdf was downloaded")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(f"sp-{number}.pdf was not downloaded,it had response status code {response.status_code}\n")
                        print(f"sp-{number}.pdf was not downloaded,it had response status code {response.status_code}")
            else:
                pages = [f'https://irannewspaper.ir/{link["href"]}' for link in main_soup.find_all("a", href=True, class_="waves-effect") if len(link["href"]) == 9 or len(link["href"]) == 10 or len(link['href']) == 11]
                print(pages)
                for i in range(len(pages)):
                    if f"sp-{i+1}.pdf" not in os.listdir(f"sp-{number}"):
                        soup = BeautifulSoup(requests.get(url=pages[i]).text, "lxml")
                        for link in soup.find_all("a", href=True):
                            if "pdf" in link["href"]:
                                download_link = link["href"]

                                response = requests.get(url=download_link)
                                if response.status_code == 200:
                                    with open(f"sp-{number}/sp-{i + 1}.pdf", "wb") as f:
                                        f.write(response.content)
                                    with open("download_results.txt", "a") as f:
                                        f.write(f"sp-{number}/sp-{i + 1}.pdf was downloaded\n")
                                    print(f"sp-{number}/sp-{i + 1}.pdf was downloaded")
                                else:
                                    with open("download_results.txt", "a") as f:
                                        f.write(f"sp-{number}/sp-{i + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                                    print(f"sp-{number}/sp-{i + 1}.pdf was not downloaded,it had response status code {response.status_code}")

    # This method will check all the magazine from n1 to n2
    def check_n1_n2_magazines(self,n1:int,n2:int):
        if n1>n2:
            c = n2
            n2 = n1
            n1 = c

        for i in range(n1,n2+1):
            self.check_magazine(i)

    #This method will check all the magazines
    def check_all_magazines(self):
        self.download_n1_n2_magazines(self.special_first,self.special_last+1)

if __name__ == "__main__":
    iran = IranNewspaper()
    iran.download_magazine(330)
