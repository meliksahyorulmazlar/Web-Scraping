# National Library Of Greece
import os
import time

import requests,lxml,json
from bs4 import BeautifulSoup
from selenium import webdriver


class NationalLibraryOfGreece:
    def __init__(self):
        self.main_page = 'http://rg-dev.nlg.gr/archive/search?lang=en&sort=old'
        self.last_page = self.get_page_count()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
        self.check_data()

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)

        self.driver = webdriver.Chrome(options=chrome_options)
    def get_page_count(self)->int:
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        page_links = [int(link.text) for link in soup.find_all("a",href=True,class_='page_link')]
        return max(page_links)

    def check_data(self):
        try:
            with open('pages.json','r') as f:
                dictionary:dict = json.load(f)
            pages_to_check = []
            for i in range(1,self.last_page):
                if str(i) not in dictionary:
                    pages_to_check.append(i)
                elif len(dictionary[str(i)]) != 32 and i != 1622:
                    pages_to_check.append(i)

            if pages_to_check:
                self.start_driver()
                print(pages_to_check)
                for i in range(len(pages_to_check)):
                    self.check_page(page_number=pages_to_check[i])
        except FileNotFoundError:
            self.check_all()


    def check_page(self,page_number:int):
        with open("pages.json","r") as f:
            dictionary:dict = json.load(f)

        page_url = f"http://rg-dev.nlg.gr/archive/search?lang=en&sort=old&page={page_number}"
        self.driver.get(page_url)
        print(page_url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        links = [link['href'] for link in soup.find_all('a', class_='iss_mtd_tlp')]

        if page_number < self.last_page:
            while len(links) != 32:
                self.driver.get(page_url)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')

                links = [link['href'] for link in soup.find_all('a', class_='iss_mtd_tlp')]
        print(links)
        print(len(links))

        newspaper_names = []
        dates = []
        for link in soup.find_all("div", class_='rs_title_elastic'):
            try:
                new_list = link.text.split()
                newspaper_names.append(new_list[0])
                dates.append(new_list[1].replace("/", "-"))
            except IndexError:
                continue

        lists = []
        for j in range(len(links)):
            newspaper_tuple = newspaper_names[j], dates[j], f"http://rg-dev.nlg.gr{links[j]}"
            lists.append(newspaper_tuple)



        if page_number == 1622:
            dictionary[page_number] = [["Μακεδονία","31-12-1969","http://rg-dev.nlg.gr/archive/item/62008"],["Ταχυδρόμος","31-12-1969","http://rg-dev.nlg.gr/archive/item/29444"],["Ταχυδρόμος","01-01-1970","http://rg-dev.nlg.gr/archive/item/29445"],["Μακεδονία","01-01-1970","http://rg-dev.nlg.gr/archive/item/62012"],["Μακεδονία","03-01-1970","http://rg-dev.nlg.gr/archive/item/62015"],["Μακεδονία","04-01-1970","http://rg-dev.nlg.gr/archive/item/62019"],["Μακεδονία","06-01-1970","http://rg-dev.nlg.gr/archive/item/62023"],["Μακεδονία","06-01-1970","http://rg-dev.nlg.gr/archive/item/29446"],["Ταχυδρόμος","07-01-1970","http://rg-dev.nlg.gr/archive/item/62025"],["Μακεδονία","07-01-1970","http://rg-dev.nlg.gr/archive/item/29447"],["Ταχυδρόμος","08-01-1970","http://rg-dev.nlg.gr/archive/item/62027"],["Μακεδονία","08-01-1970","http://rg-dev.nlg.gr/archive/item/29448"],["Ταχυδρόμος","09-01-1970","http://rg-dev.nlg.gr/archive/item/29449"],["Ταχυδρόμος","09-01-1970","http://rg-dev.nlg.gr/archive/item/62028"],["Μακεδονία","10-01-1970","http://rg-dev.nlg.gr/archive/item/62032"],["Μακεδονία","10-01-1970","http://rg-dev.nlg.gr/archive/item/29450"],["Ταχυδρόμος","11-01-1970","http://rg-dev.nlg.gr/archive/item/62034"],["Μακεδονία","11-01-1970","http://rg-dev.nlg.gr/archive/item/29451"]]
        else:
            dictionary[page_number] = lists

        with open('pages.json','w') as f:
            json.dump(dictionary,f,ensure_ascii=False,indent=4)

    def check_all(self):
        dictionary = {}
        self.start_driver()
        for i in range(1,self.last_page+1):
            page_url = f"http://rg-dev.nlg.gr/archive/search?lang=en&sort=old&page={i}"
            self.driver.get(page_url)
            print(page_url)
            soup = BeautifulSoup(self.driver.page_source,'lxml')

            links = [link['href'] for link in soup.find_all('a', class_='iss_mtd_tlp')]

            if i < self.last_page:
                while len(links) != 32:
                    self.driver.get(page_url)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')

                    links = [link['href'] for link in soup.find_all('a', class_='iss_mtd_tlp')]
            print(links)
            print(len(links))

            dates = []
            newspaper_names = []
            for link in soup.find_all("div",class_='rs_title_elastic'):
                try:
                    new_list = link.text.split()
                    newspaper_names.append(new_list[0])
                    dates.append(new_list[1].replace("/","-"))
                except IndexError:
                    continue



            lists = []
            for j in range(len(links)):
                newspaper_tuple = newspaper_names[j],dates[j],f"http://rg-dev.nlg.gr{links[j]}"
                lists.append(newspaper_tuple)


            if i == 1622:
                dictionary[i] = [["Μακεδονία","31-12-1969","http://rg-dev.nlg.gr/archive/item/62008"],["Ταχυδρόμος","31-12-1969","http://rg-dev.nlg.gr/archive/item/29444"],["Ταχυδρόμος","01-01-1970","http://rg-dev.nlg.gr/archive/item/29445"],["Μακεδονία","01-01-1970","http://rg-dev.nlg.gr/archive/item/62012"],["Μακεδονία","03-01-1970","http://rg-dev.nlg.gr/archive/item/62015"],["Μακεδονία","04-01-1970","http://rg-dev.nlg.gr/archive/item/62019"],["Μακεδονία","06-01-1970","http://rg-dev.nlg.gr/archive/item/62023"],["Μακεδονία","06-01-1970","http://rg-dev.nlg.gr/archive/item/29446"],["Ταχυδρόμος","07-01-1970","http://rg-dev.nlg.gr/archive/item/62025"],["Μακεδονία","07-01-1970","http://rg-dev.nlg.gr/archive/item/29447"],["Ταχυδρόμος","08-01-1970","http://rg-dev.nlg.gr/archive/item/62027"],["Μακεδονία","08-01-1970","http://rg-dev.nlg.gr/archive/item/29448"],["Ταχυδρόμος","09-01-1970","http://rg-dev.nlg.gr/archive/item/29449"],["Ταχυδρόμος","09-01-1970","http://rg-dev.nlg.gr/archive/item/62028"],["Μακεδονία","10-01-1970","http://rg-dev.nlg.gr/archive/item/62032"],["Μακεδονία","10-01-1970","http://rg-dev.nlg.gr/archive/item/29450"],["Ταχυδρόμος","11-01-1970","http://rg-dev.nlg.gr/archive/item/62034"],["Μακεδονία","11-01-1970","http://rg-dev.nlg.gr/archive/item/29451"],["Ταχυδρόμος","12-01-1970","http://rg-dev.nlg.gr/archive/item/29452"],["Ταχυδρόμος","13-01-1970","http://rg-dev.nlg.gr/archive/item/62035"],["Μακεδονία","13-01-1970","http://rg-dev.nlg.gr/archive/item/29453"],["Ταχυδρόμος","14-01-1970","http://rg-dev.nlg.gr/archive/item/62036"],["Μακεδονία","14-01-1970","http://rg-dev.nlg.gr/archive/item/29454"],["Ταχυδρόμος","15-01-1970","http://rg-dev.nlg.gr/archive/item/62037"],["Μακεδονία","15-01-1970","http://rg-dev.nlg.gr/archive/item/29455"],["Ταχυδρόμος","16-01-1970","http://rg-dev.nlg.gr/archive/item/62039"],["Μακεδονία","16-01-1970","http://rg-dev.nlg.gr/archive/item/29456"],["Ταχυδρόμος","17-01-1970","http://rg-dev.nlg.gr/archive/item/62040"],["Μακεδονία","17-01-1970","http://rg-dev.nlg.gr/archive/item/29457"],["Ταχυδρόμος","18-01-1970","http://rg-dev.nlg.gr/archive/item/62042"],["Μακεδονία","18-01-1970","http://rg-dev.nlg.gr/archive/item/29458"]]
            else:
                dictionary[i] = lists

            with open('pages.json', 'w') as f:
                json.dump(dictionary, f, ensure_ascii=False, indent=4)

    #The following method will get the na
    def get_newspapers(self):
        newspapers_names = []
        with open('pages.json', 'r') as f:
            dictionary: dict = json.load(f)

        for i in range(1,self.last_page+1):
            items = dictionary[str(i)]
            for item in items:
                if item[0] not in newspapers_names:
                    newspapers_names.append(item[0])
        print(newspapers_names)

    def download_newspaper(self,newspaper_name):
        with open('pages.json', 'r') as f:
            dictionary: dict = json.load(f)
        count = [1 for key in dictionary.keys()]
        newspapers = []

        if len(count) == self.last_page:
            for i in range(1, self.last_page + 1):
                items = dictionary[str(i)]
                for item in items:
                    if item[0] == newspaper_name:
                        newspapers.append(item)

        if newspapers:
            for newspaper in newspapers:
                os.makedirs(newspaper_name,exist_ok=True)

                link = newspaper[2]
                response = requests.get(url=link)
                soup = BeautifulSoup(response.text,'lxml')
                images = [f"http://rg-dev.nlg.gr{link['href']}" for link in soup.find_all('a',href=True) if 'big' in link['href']]

                filename = f"{newspaper[0]} {newspaper[1]}"

                os.mkdir(f"{newspaper_name}/{filename}")

                for i in range(len(images)):
                    image = images[i]
                    image_name = image.split("/")[-1]

                    response = image

                    response = requests.get(url=image)
                    if response.status_code == 200:
                        with open(f"{newspaper_name}/{filename}/{image_name}",'wb') as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{newspaper_name}/{filename}/{image_name} was downloaded\n")
                        print(f"{newspaper_name}/{filename}/{image_name} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{newspaper_name}/{filename}/{image_name} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{newspaper_name}/{filename}/{image_name} was not downloaded,it had response status code {response.status_code}")


    def download_newspapers(self):
        newspapers_names = []
        with open('pages.json', 'r') as f:
            dictionary: dict = json.load(f)

        for i in range(1, self.last_page + 1):
            items = dictionary[str(i)]
            for item in items:
                if item[0] not in newspapers_names:
                    newspapers_names.append(item[0])

        for newspaper in newspapers_names:
            self.download_newspaper(newspaper)

    def download_page(self,page_number)->None:
        if 1 <= page_number <= self.last_page:
            with open('pages.json','r') as f:
                dictionary = json.load(f)
            newspapers = dictionary[str(page_number)]
            for newspaper in newspapers:
                newspaper_name = newspaper[0]
                os.makedirs(newspaper_name,exist_ok=True)

                link = newspaper[2]
                response = requests.get(url=link)
                soup = BeautifulSoup(response.text,'lxml')
                images = [f"http://rg-dev.nlg.gr{link['href']}" for link in soup.find_all('a',href=True) if 'big' in link['href']]

                filename = f"{newspaper[0]} {newspaper[1]}"

                os.mkdir(f"{newspaper_name}/{filename}")

                for i in range(len(images)):
                    image = images[i]
                    image_name = image.split("/")[-1]

                    response = image

                    response = requests.get(url=image)
                    if response.status_code == 200:
                        with open(f"{newspaper_name}/{filename}/{image_name}",'wb') as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{newspaper_name}/{filename}/{image_name} was downloaded\n")
                        print(f"{newspaper_name}/{filename}/{image_name} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{newspaper_name}/{filename}/{image_name} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{newspaper_name}/{filename}/{image_name} was not downloaded,it had response status code {response.status_code}")

    def download_pages(self)->None:
        self.download_page_range(1,self.last_page)

    def download_page_range(self,n1:int,n2:int)->None:
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.download_page(i)



if __name__ == "__main__":
    nlg = NationalLibraryOfGreece()


    #['Αιών', 'Ακρόπολις', 'Σκριπ', 'Εμπρός', 'Μακεδονία', 'Ριζοσπάστης', 'Ελευθερία', 'Ταχυδρόμος']
    #nlg.download_newspaper('Αιών')
    #nlg.download_newspaper()
    #x = os.listdir()
    #print(x)
