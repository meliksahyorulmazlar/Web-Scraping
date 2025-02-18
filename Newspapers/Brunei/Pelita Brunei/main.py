# Pelita Brunei, a newspaper from Brunei
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,os,lxml
from bs4 import BeautifulSoup


class PelitaBrunei:
    def __init__(self):
        self.first_year = 1992
        self.current_year = self.return_current_year()
        self.start_driver()


    # The following method will return the current year
    def return_current_year(self)->int:
        t = datetime.datetime.now()
        return t.year

    # The following method will start the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method will download a specific year
    def download_year(self,year:int):
        if self.first_year <= year <= self.current_year:
            pdfs = self.gather_year_pdfs(year)
            if pdfs:
                os.mkdir(f"{year}")
            for pdf in pdfs:
                link = f'https://www.pelitabrunei.gov.bn/{pdf}'
                filename = pdf.split("/")[-1]
                response = requests.get(link)
                if response.status_code == 200:
                    with open(f"{year}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was downloaded.\n")
                    print(f"{year}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{year}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one year to another later year
    def download_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c

        for year in range(y1,y2+1):
            self.download_year(year)

    # The following method will download the entire archive
    def download_all(self):
        self.download_y1_y2(self.first_year,self.current_year)

    # The following method will check a specific year
    def check_year(self, year: int):
        if self.first_year <= year <= self.current_year:
            pdfs = self.gather_year_pdfs(year)
            if pdfs:
                try:
                    os.mkdir(f"{year}")
                except FileExistsError:
                    pass
            print(pdfs)
            for pdf in pdfs:
                link = f'https://www.pelitabrunei.gov.bn/{pdf}'
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(f"{year}"):
                    response = requests.get(link)
                    if response.status_code == 200:
                        with open(f"{year}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(
                                f"{year}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(
                            f"{year}/{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f'{year}/{filename} was already downloaded')

    # The following method will check from one year to another later year
    def check_y1_y2(self, y1: int, y2: int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c

        for year in range(y1, y2 + 1):
            self.check_year(year)

    # The following method will check the entire archive
    def check_all(self):
        self.check_y1_y2(self.first_year, self.current_year)




    # The following method will gather all the pdfs for a particular year
    def gather_year_pdfs(self,year:int)->list:
        if self.first_year <= year <= self.current_year:
            pages = []
            pdfs = []
            count = 0
            extra_count = 0
            website = f'https://www.pelitabrunei.gov.bn/Arkib%2520Dokumen/Forms/AllItems.aspx?RootFolder=%252fArkib%2520Dokumen%252f{year}%23PageFirstRow=50#InplviewHash9ac62886-5881-4af7-baf9-999d90c15f2a=Paged%3DTRUE-p_SortBehavior%3D0-p_Created%3D20201004%252023%253a50%253a23-p_ID%3D3046-PageFirstRow%3D{count + 1}'
            print(website)
            self.driver.get(website)
            time.sleep(5)
            while True:
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')

                new_count = 0
                for pdf in soup.find_all("a", href=True):
                    if '.pdf' in pdf['href']:
                        if pdf['href'] not in pdfs:
                            pdfs.append(pdf['href'])
                        new_count += 1
                if new_count == 0:
                    if extra_count > 0:
                        return []
                    directories = [f"https://www.pelitabrunei.gov.bn" + l['href'] for l in soup.find_all('a', class_='ms-listlink')]
                    for directory in directories:
                        self.driver.get(directory)
                        time.sleep(1)
                        new_soup = BeautifulSoup(self.driver.page_source, 'lxml')
                        for pdf in new_soup.find_all("a", href=True):
                            if '.pdf' in pdf['href']:
                                if pdf['href'] not in pdfs:
                                    pdfs.append(pdf['href'])
                                new_count += 1
                    extra_count += 1
                else:
                    tags = [tag.get_attribute('onclick') for tag in self.driver.find_elements(By.TAG_NAME, 'a') if
                            tag.get_attribute('onclick')]
                    tag = tags[-1]
                    x = tag.split('"')
                    try:
                        website = x[1]
                    except IndexError:
                        print(pdfs)
                        break
                    else:
                        t = int(website.split("FirstRow=")[1].split("&")[0])
                        pages.append(t)
                        if t < max(pages):
                            print(pdfs)
                            break
                        else:
                            if website[0] == "?":
                                website = 'https://www.pelitabrunei.gov.bn/Arkib%20Dokumen/Forms/AllItems.aspx' + website
                            self.driver.get(website)
            return pdfs


if __name__ == "__main__":
    pb = PelitaBrunei()
    pb.check_year(2015)
