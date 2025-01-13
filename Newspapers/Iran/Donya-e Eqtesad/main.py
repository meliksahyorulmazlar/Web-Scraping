#Donya-e Eqtesad front page webscraper
#Donya-e Eqtesad is a newspaper from Iran


import requests,lxml,os
from bs4 import BeautifulSoup


class DonyaEqtesad:
    def __init__(self):
        self.persian_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
        self.latest = self.find_latest()

    #This method will do the transliteration of the persian numerals on the website
    def replace_persian_numbers(self,text):
        persian_numbers = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8','۹': '9'}
        for persian, western in persian_numbers.items():
            text = text.replace(persian, western)
        return text

    #This method will find the latest number of Donya-e Eqtesad
    def find_latest(self):
        main_page = "https://donya-e-eqtesad.com"
        soup = BeautifulSoup(requests.get(url=main_page).text,"lxml")
        items = [span.text.strip() for span in soup.find_all('span')]
        for item in items:
            for char in item:
                if char in self.persian_numbers:
                    return int(self.replace_persian_numbers(item))

    #This method will download the front page of that number
    def download(self,number:int):
        i = number
        website = f"https://donya-e-eqtesad.com/روزنامه-شماره-{i}"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        day = soup.find_all("time")[-1].text
        list = [self.replace_persian_numbers(char) for char in day]
        day = "".join(list) + f" {i}"
        print(day)
        os.makedirs(day)
        image_links = [link["href"] for link in soup.find_all("a", href=True) if ".jpg" in link["href"]]
        for j in range(len(image_links)):
            response = requests.get(url=image_links[j])

            if response.status_code == 200:
                with open(f"{day}/{i}-{j + 1}.jpg", 'wb') as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{i}-{j + 1}.jpg was downloaded\n")
                print(f"{i}-{j + 1}.jpg was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{i}-{j + 1}.jpg was not downloaded,it had response status code\n")
                print(f"{i}-{j + 1}.jpg was not downloaded,it had response status code")

    #The following method will download the archive of Donya-e Eqtesad
    def download_all(self):
        for i in range(1019,self.latest+1):
            self.download(i)

    #This method will download the latest number of Donya-e Eqtesad
    def download_latest(self):
        self.download(self.latest)

    #This method will download all the numbers from n1 to n2
    #download_n1_n2(1500,1503)
    #This will download all the numbers from 1500 1501 1502 1503
    def download_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download(number=i)

    #This will download a number of Donya-e Eqtesad specified in the input
    def download_number(self,number:int):
        self.download(number)

    # The following method will check to see if the pdf has been downloaded or not
    def check_download(self,number:int):
        i = number
        website = f"https://donya-e-eqtesad.com/روزنامه-شماره-{i}"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        day = soup.find_all("time")[-1].text
        list = [self.replace_persian_numbers(char) for char in day]
        day = "".join(list) + f" {i}"
        print(day)
        try:
            os.mkdir(day)
        except FileExistsError:
            pass
        image_links = [link["href"] for link in soup.find_all("a", href=True) if ".jpg" in link["href"]]
        for j in range(len(image_links)):
            filename = f"{i}-{j + 1}.jpg"
            if filename not in os.listdir(day):
                response = requests.get(url=image_links[j])

                if response.status_code == 200:
                    with open(f"{day}/{i}-{j + 1}.jpg", 'wb') as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{i}-{j + 1}.jpg was downloaded\n")
                    print(f"{i}-{j + 1}.jpg was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{i}-{j + 1}.jpg was not downloaded,it had response status code\n")
                    print(f"{i}-{j + 1}.jpg was not downloaded,it had response status code")

    #The following method will check the entire archive of Donya-e Eqtesad
    def check_all(self):
        for i in range(1019,self.latest+1):
            self.check_download(i)

    #This method will check the latest number of Donya-e Eqtesad
    def check_latest(self):
        self.check_download(self.latest)

    #This method will download all the numbers from n1 to n2
    #download_n1_n2(1500,1503)
    #This will download all the numbers from 1500 1501 1502 1503
    def check_n1_n2(self,n1:int,n2:int):
        if n1>n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.check_download(number=i)

    
if __name__ == "__main__":
    de = DonyaEqtesad()
    de.download_all()
