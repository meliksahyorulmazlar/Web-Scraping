#Plovdiv Library
import os,time,requests,lxml
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class PlovdivLibrary:
    def __init__(self):
        self.site = "https://digital.libplovdiv.com/en"
        self.start_webdriver()
        self.categories = []
        self.periodicals = {}
        self.gather_categories()
        self.gather_periodicals()

    # The following method will start the selenium webdriver
    def start_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=options)

    # The following method will gather all the categories
    def gather_categories(self):
        self.driver.get(self.site)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        not_categories = ['/en/v/contact', '/en/v/terms-of-use', '/en/v/privacy-policy', '/en/v/cookie-policy','http://www.libplovdiv.com','/en/v/faq']
        self.categories = [cat['href'].split("/")[-1] for cat in soup.find_all('a',href=True) if '/v/' in cat['href'] and cat['href'] not in not_categories]

    # The following method will print all the categories the website has
    def print_categories(self):
        for category in self.categories:
            print(category)

    # The following method will download a particular category
    def download_category(self,category:str):
        if category == 'periodicals':
            self.download_categories()
        elif category in self.categories:
            os.mkdir(category)
            site = f'https://digital.libplovdiv.com/en/v/{category}'
            self.driver.get(site)
            time.sleep(3)
            sentence = self.driver.find_element(By.ID, 'result').text.split()
            total = int(sentence[-1])
            per = int(sentence[-3])
            if per == total:
                pages = 1
            else:
                pages = self.find_page_count(per, total)
            for page in range(1, pages + 1):
                site = f"https://digital.libplovdiv.com/en/v/{category}?page={page}#result"
                print(site)
                self.driver.get(site)
                time.sleep(3)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                items = [item['href'] for item in soup.find_all('a', href=True) if '/en/view/' in item['href']]
                texts = [item.text for item in soup.find_all(class_='text')]
                new_items = []
                for i in range(len(items)):
                    tpl = texts[i], items[i]
                    new_items.append(tpl)
                items = new_items
                for tpl in items:
                    file_text = tpl[0]
                    item = tpl[1]
                    site = f'https://digital.libplovdiv.com{item}'
                    self.driver.get(site)
                    while True:
                        try:
                            tag = self.driver.find_element(By.TAG_NAME, 'iframe')
                            break
                        except selenium.common.exceptions.NoSuchElementException:
                            time.sleep(1)
                            continue
                    source_tag = tag.get_attribute('src')
                    if source_tag == 'https://digital.libplovdiv.com/3rdparty/mirador/index.html':
                        continue
                    else:
                        file_link = 'https://digital.libplovdiv.com' + source_tag.split("=")[1].replace("&locale", '')
                        while True:
                            try:
                                tag = self.driver.find_element(By.TAG_NAME, 'h1')
                                break
                            except selenium.common.exceptions.NoSuchElementException:
                                time.sleep(1)
                                continue
                        filetype = file_link.split(".")[-1]
                        filename = file_text + "." + filetype
                        response = requests.get(url=file_link)
                        if response.status_code == 200:
                            with open(f"{category}/{filename}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{filename} was downloaded.\n")
                            print(f"{filename} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                            print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the categories on the archive
    def download_categories(self):
        for category in self.categories:
            self.download_category(category)

    # The following method will find how many pages there are on the archive
    def find_page_count(self,per:int,total:int):
        if total % per == 0:
            return  total //per
        return (total//per) + 1

    # The following method will check a category
    def check_category(self,category:str):
        if category == 'periodicals':
            self.check_periodicals()
        elif category in self.categories:
            try:
                os.mkdir(category)
            except FileExistsError:
                pass
            site = f'https://digital.libplovdiv.com/en/v/{category}'
            self.driver.get(site)
            time.sleep(3)
            sentence = self.driver.find_element(By.ID, 'result').text.split()
            total = int(sentence[-1])
            per = int(sentence[-3])
            if per == total:
                pages = 1
            else:
                pages = self.find_page_count(per, total)
            for page in range(1, pages + 1):
                site = f"https://digital.libplovdiv.com/en/v/{category}?page={page}#result"
                self.driver.get(site)
                time.sleep(3)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                items = [item['href'] for item in soup.find_all('a', href=True) if '/en/view/' in item['href']]
                texts = [item.text for item in soup.find_all(class_='text')]
                new_items = []
                for i in range(len(items)):
                    tpl = texts[i],items[i]
                    new_items.append(tpl)
                items = new_items
                for tpl in items:
                    file_text = tpl[0]
                    item = tpl[1]
                    site = f'https://digital.libplovdiv.com{item}'
                    self.driver.get(site)
                    while True:
                        try:
                            tag = self.driver.find_element(By.TAG_NAME, 'iframe')
                            break
                        except selenium.common.exceptions.NoSuchElementException:
                            time.sleep(1)
                            continue
                    source_tag = tag.get_attribute('src')
                    if source_tag == 'https://digital.libplovdiv.com/3rdparty/mirador/index.html':
                        continue
                    else:
                        file_link = 'https://digital.libplovdiv.com' + source_tag.split("=")[1].replace("&locale", '')
                        while True:
                            try:
                                tag = self.driver.find_element(By.TAG_NAME, 'h1')
                                break
                            except selenium.common.exceptions.NoSuchElementException:
                                time.sleep(1)
                                continue
                        filetype = file_link.split(".")[-1]
                        filename = file_text + "." + filetype
                        if filename not in os.listdir(category):
                            response = requests.get(url=file_link)
                            if response.status_code == 200:
                                with open(f"{category}/{filename}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{filename} was downloaded.\n")
                                print(f"{filename} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                                print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will check all the categories on the library archive
    def check_categories(self):
        for category in self.categories:
            self.check_category(category)

    # The following method will download the periodicals
    def download_periodicals(self):
        for periodical in self.periodicals:
            self.download_periodical(periodical)

    # The following method will check the periodicals
    def check_periodicals(self):
        for periodical in self.periodicals:
            self.check_periodical(periodical)

    # The following method will gather all the periodicals
    def gather_periodicals(self):
        site = 'https://digital.libplovdiv.com/en/v/periodicals'
        self.driver.get(site)
        while True:
            try:
                sentence = self.driver.find_element(By.ID, 'result')
                break
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(0.1)
                continue
        sentence = sentence.text.split()
        total = int(sentence[-1])
        per = int(sentence[-3])
        pages = self.find_page_count(per, total)
        for i in range(1,pages+1):
            site = f'https://digital.libplovdiv.com/en/v/periodicals?page={i}#result'
            self.driver.get(site)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            names = [(link.text, link['href']) for link in soup.find_all('a', href=True) if '/en/view/' in link['href']]
            for name in names:
                code = name[1].split("/")[-1]
                key = name[0] +'-'+ code
                self.periodicals[key] = name[1]
                print(key)

    # The following method will download a particular periodical
    def download_periodical(self, periodical: str):
        if periodical in self.periodicals:
            os.makedirs(f'periodicals/{periodical}')
            site = f'https://digital.libplovdiv.com{self.periodicals[periodical]}'
            self.driver.get(site)
            time.sleep(3)
            sentence = self.driver.find_element(By.ID, 'result').text.split()
            total = int(sentence[-1])
            per = int(sentence[-3])
            if per == total:
                pages = 1
            else:
                pages = self.find_page_count(per, total)
            print(pages)
            for page in range(1, pages + 1):
                site = f"https://digital.libplovdiv.com{self.periodicals[periodical]}?page={page}#result"
                print(site)
                self.driver.get(site)
                time.sleep(3)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                items = [item['href'] for item in soup.find_all('a', href=True) if '/en/view/' in item['href']]
                print(periodical, items)
                for item in items:
                    site = f'https://digital.libplovdiv.com{item}'
                    self.driver.get(site)
                    while True:
                        try:
                            tag = self.driver.find_element(By.TAG_NAME, 'iframe')
                            break
                        except selenium.common.exceptions.NoSuchElementException:
                            time.sleep(1)
                            continue
                    source_tag = tag.get_attribute('src')
                    if source_tag == 'https://digital.libplovdiv.com/3rdparty/mirador/index.html':
                        continue
                    else:
                        file_link = 'https://digital.libplovdiv.com' + source_tag.split("=")[1].replace("&locale", '')
                        while True:
                            try:
                                tag = self.driver.find_element(By.TAG_NAME, 'h1')
                                break
                            except selenium.common.exceptions.NoSuchElementException:
                                time.sleep(1)
                                continue
                        filetype = file_link.split(".")[-1]
                        filename = tag.text + "." + filetype
                        print(filename)
                        response = requests.get(url=file_link)
                        if response.status_code == 200:
                            with open(f"periodicals/{periodical}/{filename}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{periodical}/{filename} was downloaded.\n")
                            print(f"{periodical}/{filename} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{periodical}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                            print(f"{periodical}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will check a particular periodical
    def check_periodical(self, periodical: str):
        if periodical in self.periodicals:
            try:
                os.makedirs(f'periodicals/{periodical}')
            except FileExistsError:
                pass
            site = f'https://digital.libplovdiv.com{self.periodicals[periodical]}'
            self.driver.get(site)
            time.sleep(3)
            sentence = self.driver.find_element(By.ID, 'result').text.split()
            total = int(sentence[-1])
            per = int(sentence[-3])
            if per == total:
                pages = 1
            else:
                pages = self.find_page_count(per, total)
            for page in range(1, pages + 1):
                site = f"https://digital.libplovdiv.com{self.periodicals[periodical]}?page={page}#result"
                self.driver.get(site)
                time.sleep(3)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                items = [item['href'] for item in soup.find_all('a', href=True) if '/en/view/' in item['href']]
                for item in items:
                    site = f'https://digital.libplovdiv.com{item}'
                    self.driver.get(site)
                    while True:
                        try:
                            tag = self.driver.find_element(By.TAG_NAME, 'iframe')
                            break
                        except selenium.common.exceptions.NoSuchElementException:
                            time.sleep(1)
                            continue
                    source_tag = tag.get_attribute('src')
                    if source_tag == 'https://digital.libplovdiv.com/3rdparty/mirador/index.html':
                        continue
                    else:
                        file_link = 'https://digital.libplovdiv.com' + source_tag.split("=")[1].replace("&locale", '')
                        while True:
                            try:
                                tag = self.driver.find_element(By.TAG_NAME, 'h1')
                                break
                            except selenium.common.exceptions.NoSuchElementException:
                                time.sleep(1)
                                continue
                        filetype = file_link.split(".")[-1]
                        filename = tag.text +"."+ filetype
                        print(filename)
                        if filename not in os.listdir(f'periodicals/{periodical}'):
                            response = requests.get(url=file_link)
                            if response.status_code == 200:
                                with open(f"periodicals/{periodical}/{filename}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{periodical}/{filename} was downloaded.\n")
                                print(f"{periodical}/{filename} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{periodical}/{filename} was not downloaded, it had response status code {response.status_code}.\n")
                                print(f"{periodical}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will print all the periodicals
    def print_periodicals(self):
        for periodical in self.periodicals:
            print(periodical)


if __name__ == "__main__":
    pl = PlovdivLibrary()
    pl.download_category('books')
