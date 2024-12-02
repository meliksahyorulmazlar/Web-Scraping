#KCNA Watch is an outlet that shows what is going in North Korea
import time

from bs4 import BeautifulSoup
import requests,os,lxml,datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

class KcnaWatch:
    def __init__(self):
        self.main_page = "https://kcnawatch.xyz"
        self.downloadable = {}
        self.today = self.return_today()
        self.start_driver()
        self.find_papers()

    # This method will start the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=chrome_options)


    # This method returns today
    def return_today(self)->datetime.datetime:
        today = datetime.datetime.now()
        day = today.day
        month = today.month
        year = today.year
        return datetime.datetime(day=day,month=month,year=year)


    # This method will find all the North Korean Newspapers or Magazines that can be downloaded
    def find_papers(self):
        self.driver.get(url=self.main_page)

        periodicals = self.driver.find_element(By.LINK_TEXT,"Periodicals")
        periodicals.click()

        html_content = self.driver.page_source

        soup = BeautifulSoup(html_content,"lxml")

        delete = ["Rodong PDFs (Discontinued)","Pyongyang Times PDF"]
        periodicals = [(link.text,link["href"]) for link in soup.find_all("a",href=True) if "periodicals" in link["href"] and link.text not in delete]

        for periodical in periodicals:
            self.downloadable[periodical[0]] = periodical[1]

    # The following method will print the names of all the newspapers/magazines that can be downloaded
    def print_names(self):
        for key in self.downloadable:
            print(key)

    # The following method will download a specific newspaper/magazine
    def download_newspaper(self,newspaper:str):
        if newspaper in self.downloadable:
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            page = self.downloadable[newspaper]
            self.driver.get(page)

            time.sleep(1)
            more = self.driver.find_element(By.LINK_TEXT, "More Periodicals")
            while True:
                try:
                    self.driver.execute_script("window.scrollBy(0, 900);")
                    more = self.driver.find_element(By.LINK_TEXT, "More Periodicals")
                    more.click()
                    time.sleep(0.5)
                except exceptions.NoSuchElementException:
                    break
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            links = [link['href'] for link in soup.find_all("a", href=True) if '/periodical/' in link['href']]
            new_links = []
            for link in links:
                if link not in new_links:
                    new_links.append(link)
            for link in new_links:
                self.driver.get(link)
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')

                for link in soup.find_all("a", href=True):
                    if ".pdf" in link['href']:
                        filename = link['href'].split('/')[-1]
                        response = requests.get(link['href'])
                        if response.status_code == 200:
                            with open(f'{newspaper}/{filename}', 'wb') as f:
                                f.write(response.content)
                            with open("download_results.txt", 'a') as f:
                                f.write(f"{newspaper}/{filename} was downloaded.\n")
                            print(f"{newspaper}/{filename} was downloaded.")
                        else:
                            with open("download_results.txt", 'a') as f:
                                f.write(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the newspapers/magazines
    def download_newspapers(self):
        for newspaper in self.downloadable:
            self.download_newspaper(newspaper)

    # The following method will check a specific newspaper for any missing newspapers
    def check_newspaper(self,newspaper:str):
        if newspaper in self.downloadable:
            try:
                files = os.listdir(newspaper)
            except FileNotFoundError:
                self.download_newspaper(newspaper)
            else:
                page = self.downloadable[newspaper]
                self.driver.get(page)

                time.sleep(1)
                more = self.driver.find_element(By.LINK_TEXT, "More Periodicals")
                while True:
                    try:
                        self.driver.execute_script("window.scrollBy(0, 900);")
                        more = self.driver.find_element(By.LINK_TEXT, "More Periodicals")
                        more.click()
                        time.sleep(0.5)  # Allow time for new content to load
                    except exceptions.NoSuchElementException:
                        break
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                links = [link['href'] for link in soup.find_all("a", href=True) if '/periodical/' in link['href']]
                new_links = []
                for link in links:
                    if link not in new_links:
                        new_links.append(link)
                for link in new_links:
                    self.driver.get(link)
                    time.sleep(1)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')

                    for link in soup.find_all("a", href=True):
                        if ".pdf" in link['href']:
                            filename = link['href'].split('/')[-1]
                            if filename not in files:
                                response = requests.get(link['href'])
                                if response.status_code == 200:
                                    with open(f'{newspaper}/{filename}', 'wb') as f:
                                        f.write(response.content)
                                    with open("download_results.txt", 'a') as f:
                                        f.write(f"{newspaper}/{filename} was downloaded.\n")
                                    print(f"{newspaper}/{filename} was downloaded.")
                                else:
                                    with open("download_results.txt", 'a') as f:
                                        f.write(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                                    print(f"{newspaper}/{filename} was not downloaded, it had response status code {response.status_code}")


    # This method will check all the newspapers for missing newspapers
    def check_newspapers(self):
        for newspaper in self.downloadable:
            self.download_newspaper(newspaper)

    # This method will download the broadcasts on North Korean National Television
    def download_tv_broadcast(self,date:datetime.datetime):
        if datetime.datetime(day=23,month=10,year=2017) <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            if day < 10:
                day = f"0{day}"

            if month < 10:
                month = f"0{month}"

            format = f"{day}-{month}-{year}"
            website = f'https://kcnawatch.xyz/kctv-archive/?start={format}&end={format}'
            self.driver.get(website)
            time.sleep(1)

            soup = BeautifulSoup(self.driver.page_source,'lxml')
            broadcasts = [f'https://kcnawatch.xyz{link["href"]}' for link in soup.find_all("a",href=True) if "kctv" in link['href'] and link['href'] !='https://kcnawatch.xyz/kctv-archive/']
            broadcasts = list(set(broadcasts))

            for broadcast in broadcasts:
                self.driver.get(broadcast)
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source,'lxml')

                videos = [video['src'] for video in soup.find_all('source',src=True)]

                file_format = f"{day}-{month}-{year}"
                try:
                    os.mkdir(file_format)
                except FileExistsError:
                    pass
                print(broadcast,videos)
                for video in videos:
                    response = requests.get(url=video)
                    filename = video.split("/")[-1]
                    if response.status_code == 200:
                        with open(f"{file_format}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('tv_results.txt','a') as f:
                            f.write(f"{file_format} {filename} was downloaded.\n")
                        print(f"{file_format} {filename} was downloaded.")
                    else:
                        with open('tv_results.txt','a') as f:
                            f.write(f"{file_format} {filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{file_format} {filename} was not downloaded,it had response status code {response.status_code}")

    # This method will download all the tv broadcasts from one day to another
    def download_tv_broadcast_range(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c

        one_day = datetime.timedelta(days=1)
        while d1 <= d2:
            self.download_tv_broadcast(d1)
            d1 += one_day

    # The following method will download all the tv broadcasts from the 23rd October till today
    def download_all_tv_broadcasts(self):
        d1 = datetime.datetime(day=23,month=10,year=2017)
        d2 = self.today
        self.download_tv_broadcast_range(d1,d2)



if __name__ == "__main__":
    kcna = KcnaWatch()
    kcna.download_tv_broadcast(date=datetime.datetime(day=1,month=1,year=2019))


