# The National Library of Liechtenstein webscraper
import time

import requests,os,lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class NationalLibraryoLiechtenstein:
    def __init__(self):
        self.main_page = 'https://www.eliechtensteinensia.li/viewer/index/'
        self.categories = {}
        self.start_driver()
        self.gather_categories()

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)

        self.driver = webdriver.Chrome(options=chrome_options)


    def gather_categories(self):
        self.driver.get(url=self.main_page)
        time.sleep(0.5)
        self.driver.execute_script("window.scrollBy(0, 800);")
        items = [item for item in self.driver.find_elements(By.TAG_NAME, 'a')]
        categories = []
        for item in items:
            if 'themen' in item.get_attribute('href'):
                categories.append(item)
        categories = [category for category in categories if category.get_attribute('title')]

        for c in categories:
            self.categories[c.get_attribute('title')] = c.get_attribute('href')
        print(self.categories)

    #This method will print out all the categories
    def print_categories(self):
        for c in self.categories:
            print(c)

    # This method will find the page count
    def return_page_count(self,number:int):
        if number < 10:
            return 1
        elif number % 10 == 0:
            return number//10
        else:
            return (number // 10)+1

    # The following method will download a specific category
    def download_category(self,category:str):
        if category in self.categories:
            os.mkdir(category)
            self.driver.get(self.categories[category])

            items = [int(item.text.split(" ")[1].strip(')').strip('(')) for item in self.driver.find_elements(By.CLASS_NAME, 'collection__top-element')]
            number = items[0]
            page_count = self.return_page_count(number)
            print(page_count)

            for page_number in range(1, page_count + 1):
                site = f"https://www.eliechtensteinensia.li/viewer/search/-/-/{page_number}/-/MD_KNOWLEDGEAREA%3A{category.lower()}/"
                self.driver.get(url=site)
                items = [item for item in self.driver.find_elements(By.TAG_NAME, 'a') if
                         item.get_attribute('title') and '/1/LOG_0000/' in item.get_attribute('href')]
                x = []
                for item in items:
                    tpl = item.get_attribute('title'), item.get_attribute('href')
                    if tpl not in x:
                        x.append(tpl)

                for item in x:
                    title = item[0]
                    url = item[1]
                    code = url.split('/')[-4]
                    if 'image' in url:
                        pdf_link = f'https://www.eliechtensteinensia.li/viewer/api/v1/records/{code}/pdf/'
                        response = requests.get(pdf_link)
                        if response.status_code == 200:
                            with open(f"{category}/{code}.pdf", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{category}/{code}.pdf was downloaded.\n")
                                print(f"{category}/{code}.pdf was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{category}/{code}.pdf was not downloaded,it had response status code {response.status_code}.\n")
                                print(f"{category}/{code}.pdf was not downloaded,it had response status code {response.status_code}.")
                    elif 'toc' in url:
                        os.mkdir(f'{category}/{title}_{code}')
                        xml_website = f'https://www.eliechtensteinensia.li/viewer/metsresolver?id={code}'
                        self.driver.get(xml_website)
                        soup = BeautifulSoup(self.driver.page_source,'xml')
                        links = [link['xlink:href'] for link in soup.find_all('mets:mptr') if 'xlink:href' in link.attrs]
                        for link in links:
                            link = link.split("=")[-1]
                            pdf_link = f'https://www.eliechtensteinensia.li/viewer/api/v1/records/{link}/pdf/'
                            response = requests.get(pdf_link)
                            if response.status_code == 200:
                                with open(f"{category}/{title}_{code}/{link}.pdf", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{category}/{title}_{code}/{link}.pdf.pdf was downloaded.\n")
                                    print(f"{category}/{title}_{code}/{link}.pdf.pdf was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{category}/{title}_{code}/{link}.pdf.pdf was not downloaded,it had response status code {response.status_code}.\n")
                                print(f"{category}/{title}_{code}/{link}.pdf.pdf was not downloaded,it had response status code {response.status_code}.")

    # This method checks if the all any new pdfs have been added and it will download them
    def check_category(self, category: str):
        if category in self.categories:
            try:
                files = os.listdir(category)
            except FileNotFoundError:
                self.download_category(category)
            else:
                self.driver.get(self.categories[category])

                items = [int(item.text.split(" ")[1].strip(')').strip('(')) for item in self.driver.find_elements(By.CLASS_NAME, 'collection__top-element')]
                number = items[0]
                page_count = self.return_page_count(number)
                print(page_count)

                for page_number in range(1, page_count + 1):
                    site = f"https://www.eliechtensteinensia.li/viewer/search/-/-/{page_number}/-/MD_KNOWLEDGEAREA%3A{category.lower()}/"
                    self.driver.get(url=site)
                    items = [item for item in self.driver.find_elements(By.TAG_NAME, 'a') if
                             item.get_attribute('title') and '/1/LOG_0000/' in item.get_attribute('href')]
                    x = []
                    for item in items:
                        tpl = item.get_attribute('title'), item.get_attribute('href')
                        if tpl not in x:
                            x.append(tpl)

                    for item in x:
                        title = item[0]
                        url = item[1]
                        code = url.split('/')[-4]
                        if 'image' in url:
                            if f"{code}.pdf" not in os.listdir(category):
                                pdf_link = f'https://www.eliechtensteinensia.li/viewer/api/v1/records/{code}/pdf/'
                                response = requests.get(pdf_link)
                                if response.status_code == 200:
                                    with open(f"{category}/{code}.pdf", 'wb') as f:
                                        f.write(response.content)
                                    with open('download_results.txt', 'a') as f:
                                        f.write(f"{category}/{code}.pdf was downloaded.\n")
                                        print(f"{category}/{code}.pdf was downloaded.")
                                else:
                                    with open('download_results.txt', 'a') as f:
                                        f.write(f"{category}/{code}.pdf was not downloaded,it had response status code {response.status_code}.\n")
                                        print(f"{category}/{code}.pdf was not downloaded,it had response status code {response.status_code}.")
                        elif 'toc' in url:
                            try:
                                os.mkdir(f'{category}/{title}_{code}')
                            except FileExistsError:
                                pass
                            xml_website = f'https://www.eliechtensteinensia.li/viewer/metsresolver?id={code}'
                            self.driver.get(xml_website)
                            soup = BeautifulSoup(self.driver.page_source, 'xml')
                            links = [link['xlink:href'] for link in soup.find_all('mets:mptr') if'xlink:href' in link.attrs]
                            for link in links:
                                link = link.split("=")[-1]
                                pdf_link = f'https://www.eliechtensteinensia.li/viewer/api/v1/records/{link}/pdf/'
                                response = requests.get(pdf_link)
                                if f"{link}.pdf" not in os.listdir(f'{category}/{title}_{code}'):
                                    if response.status_code == 200:
                                        with open(f"{category}/{title}_{code}/{link}.pdf", 'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt', 'a') as f:
                                            f.write(f"{category}/{title}_{code}/{link}.pdf.pdf was downloaded.\n")
                                            print(f"{category}/{title}_{code}/{link}.pdf.pdf was downloaded.")
                                    else:
                                        with open('download_results.txt', 'a') as f:
                                            f.write(f"{category}/{title}_{code}/{link}.pdf.pdf was not downloaded,it had response status code {response.status_code}.\n")
                                        print(f"{category}/{title}_{code}/{link}.pdf.pdf was not downloaded,it had response status code {response.status_code}.")

    # The following method will download all the categories
    def download_categories(self):
        for category in self.categories:
            self.download_category(category)

    # The following method will check all the categories
    def check_categories(self):
        for category in self.categories:
            self.check_category(category)

if __name__ == "__main__":
    nll = NationalLibraryoLiechtenstein()
    nll.download_categories()
