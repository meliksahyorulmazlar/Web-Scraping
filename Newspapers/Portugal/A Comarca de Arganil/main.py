#A Comarca de Arganil is a newspaper in Portugal


import requests,os,lxml
from bs4 import BeautifulSoup

class AComarcadeArganil:
    def __init__(self):
        self.name = "A Comarca de Arganil"
        self.page_count = 0
        self.find_pages()
        self.minimum = 0
        self.find_minimum()
        self.maximum = 0
        self.find_maximum()


    #This method will find how many pages there are on the webpage
    def find_pages(self):
        website = "https://www.acomarcadearganil.cm-arganil.pt/edicoes-da-comarca/"

        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        numbers = [int(number.text) for number in soup.find_all("a",href=True,class_="page-numbers") if number.text != '']
        self.page_count = max(numbers)


    # This method will the minimum number of the newspaper
    def find_minimum(self):
        website = "https://www.acomarcadearganil.cm-arganil.pt/edicoes-da-comarca/page/1/"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")

        numbers = [int(number.text.strip("A Comarca de Arganil ")) for number in soup.find_all("h2",class_="entry-title")]

        self.minimum = min(numbers)


    #This method will the maximum number of the newspaper
    def find_maximum(self):
        website = f"https://www.acomarcadearganil.cm-arganil.pt/edicoes-da-comarca/page/{self.page_count}/"

        soup = BeautifulSoup(requests.get(url=website).text, "lxml")

        numbers = [int(number.text.strip("A Comarca de Arganil ")) for number in soup.find_all("h2", class_="entry-title")]

        self.maximum = max(numbers)

    #This method will download a specific given number of the newspaper
    def download_number(self,number:int):
        if self.minimum <= number <= self.maximum:
            try:
                os.mkdir(self.name)
            except FileExistsError:
                pass
            dictionary = {11881:"11881-20090422.pdf",11882:"20090429",11883:"20090506",11884:"20090513",11885:"20090520",11886:"20090527",11887:"20090603",11888:"0090610"}
            if number in dictionary:
                filename = f"{number}-{dictionary[number]}.pdf"
            else:
                page_number = self.find_current_page(number)
                website = f"https://www.acomarcadearganil.cm-arganil.pt/edicoes-da-comarca/page/{page_number}/"
                soup = BeautifulSoup(requests.get(url=website).text,"lxml")
                divs = [div.text.replace("\n","") for div in soup.find_all("div") if "Data de Edição: " in div.text]
                print(divs[::-1])
                dates = []
                index = len(divs)-1
                while len(dates) <60:
                    date = divs[index].strip("Data de Edição: ").replace("/","")
                    dates.append(date)
                    index -= 1
                dates = dates[::-1]
                remainder = number%60
                if remainder == 0:
                    filename = f'{number}-{dates[59]}.pdf'
                else:
                    filename = f'{number}-{dates[remainder - 1]}.pdf'

            pdf_page = f"https://www.acomarcadearganil.cm-arganil.pt/comarcafiles/{number}/{number}.pdf"

            response = requests.get(url=pdf_page)

            if response.status_code == 200:
                with open(f"{self.name}/{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{number} was downloaded\n")
                print(f"{number} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{number} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{number} was not downloaded,it had response status code {response.status_code}")


    # This method will find the current page that numbered newspaper is in
    def find_current_page(self,number:int):
        if number % 60 == 0:
            return number//60

        if number < 60:
            return 1

        if number >60:
            result = number//60
            return result+1

    # The following method will download all the numbers from n1 to n2
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for number in range(n1,n2+1):
            self.download_number(number)

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(self.minimum,self.maximum)

    #The following method will check if a number was downloaded or not
    def check_number(self,number:int):
        if self.minimum <= number <= self.maximum:
            try:
                os.mkdir(self.name)
            except FileExistsError:
                pass
            dictionary = {11881:"11881-20090422.pdf",11882:"20090429",11883:"20090506",11884:"20090513",11885:"20090520",11886:"20090527",11887:"20090603",11888:"0090610"}
            if number in dictionary:
                filename = f"{number}-{dictionary[number]}.pdf"
            else:
                page_number = self.find_current_page(number)
                website = f"https://www.acomarcadearganil.cm-arganil.pt/edicoes-da-comarca/page/{page_number}/"
                soup = BeautifulSoup(requests.get(url=website).text,"lxml")
                divs = [div.text.replace("\n","") for div in soup.find_all("div") if "Data de Edição: " in div.text]
                print(divs[::-1])
                dates = []
                index = len(divs)-1
                while len(dates) <60:
                    date = divs[index].strip("Data de Edição: ").replace("/","")
                    dates.append(date)
                    index -= 1
                dates = dates[::-1]
                remainder = number%60
                if remainder == 0:
                    filename = f'{number}-{dates[59]}.pdf'
                else:
                    filename = f'{number}-{dates[remainder - 1]}.pdf'

            pdf_page = f"https://www.acomarcadearganil.cm-arganil.pt/comarcafiles/{number}/{number}.pdf"

            if filename not in os.listdir(self.name):
                response = requests.get(url=pdf_page)

                if response.status_code == 200:
                    with open(f"{self.name}/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{number} was downloaded\n")
                    print(f"{number} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{number} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{number} was not downloaded,it had response status code {response.status_code}")

    #The following method will check from one number to another larger number
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.check_number(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(self.minimum,self.maximum)



if __name__ == "__main__":
    aca = AComarcadeArganil()
    aca.download_n1_n2(11883,aca.maximum)
