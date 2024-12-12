# Archivi.ng archive

import requests,lxml,os,time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class ArchiviNG:
    def __init__(self):
        self.main_page = 'https://archivi.ng/search?page=1'
        self.start_driver()

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.max_count = self.get_max_page()

    def get_max_page(self)->int:
        self.driver.get(self.main_page)
        time.sleep(3)
        self.driver.execute_script("window.scrollBy(0, 1000);")
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        page_counts = []

        for b in soup.find_all('button', attrs={"aria-label": True}):
            if len(b.text) >=3:
                try:
                    page_count = int(b.text)
                    page_counts.append(page_count)
                except ValueError:
                    pass

        page_count = max(page_counts)
        return page_count

    # The following method will download a page number between 1 and the max page number inclusive
    def download_page(self,page_number:int):
        if 1<= page_number <= self.max_count:
            site = self.main_page.replace('1',str(page_number))
            self.driver.get(site)
            dates = [item.text for item in self.driver.find_elements(By.CLASS_NAME,'item--desc')]
            images = self.driver.find_elements(By.TAG_NAME,'img')
            images = [image.get_attribute('src') for image in images if 'amazon' in image.get_attribute('src')]
            for i  in range(len(images)):
                image = images[i]
                list_form = image.split("%20")
                filename = list_form[-1]
                date_form = dates[i].split(",")[0]
                try:
                    os.mkdir(date_form)
                except FileExistsError:
                    pass
                response = requests.get(image)
                if response.status_code == 200:
                    with open(f"{date_form}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{date_form}/{filename} was downloaded.\n")
                    print(f"{date_form}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{date_form}/{filename} was downloaded,it had response status code {response.status_code}.\n")
                    print(f"{date_form}/{filename} was downloaded,it had response status code {response.status_code}.")

    # This method will download all the pages
    def download_pages(self):
        for i in range(1,self.max_count+1):
            self.download_page(i)

    # The following method will check if all the images were downloaded or nor
    def check_page(self,page_number:int):
        if 1 <= page_number <= self.max_count:
            site = self.main_page.replace('1', str(page_number))
            self.driver.get(site)
            dates = [item.text for item in self.driver.find_elements(By.CLASS_NAME, 'item--desc')]
            images = self.driver.find_elements(By.TAG_NAME, 'img')
            images = [image.get_attribute('src') for image in images if 'amazon' in image.get_attribute('src')]
            for i in range(len(images)):
                image = images[i]
                list_form = image.split("%20")
                filename = list_form[-1]
                date_form = dates[i].split(",")[0]
                try:
                    os.mkdir(date_form)
                except FileExistsError:
                    pass
                if filename not in os.listdir(date_form):
                    response = requests.get(image)
                    if response.status_code == 200:
                        with open(f"{date_form}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{date_form}/{filename} was downloaded.\n")
                        print(f"{date_form}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(
                                f"{date_form}/{filename} was downloaded,it had response status code {response.status_code}.\n")
                        print(f"{date_form}/{filename} was downloaded,it had response status code {response.status_code}.")

    # The following method will check all the pages
    def check_pages(self):
        for i in range(1,self.max_count+1):
            self.check_page(i)

if __name__ == "__main__":
    an = ArchiviNG()
    an.check_pages()
