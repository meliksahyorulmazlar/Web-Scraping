# Cyprus Press Information Office
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,os,lxml
from bs4 import BeautifulSoup



class CyprusPressInformationOffice:
    def __init__(self):
        self.start_driver()
        self.driver.get('https://www.pressarchive.cy/s/en/page/homepage')
        self.newspaper_dictionary = {}
        self.gather_newspapers()

    # The following method starts the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method gathers all the newspapers
    def gather_newspapers(self):
        self.driver.execute_script("window.scrollBy(0, 500);")
        buttons = [b for b in self.driver.find_elements(By.TAG_NAME,'button') if b.text.strip() == 'Accept & Close']
        self.driver.execute_script("arguments[0].scrollIntoView(true);", buttons[0])
        buttons[0].click()

        self.driver.get(url='https://www.pressarchive.cy/s/en/find?q=&limit%5Bresource_class_s%5D%5B0%5D=dctype:Collection')
        self.driver.execute_script("window.scrollBy(0, 1500);")
        pages = self.driver.find_element(By.CLASS_NAME,'page-count')
        page_count = pages.text.replace("of ","")
        for i in range(1,int(page_count)+1):
            site = f'https://www.pressarchive.cy/s/en/find?q=&limit%5Bresource_class_s%5D%5B0%5D=dctype:Collection&page={i}'
            self.driver.get(site)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            names = [p.text.replace('\n', '') for p in soup.find_all('h1') if "\n" in p.text]
            new_papers = [paper['href'] for paper in soup.find_all('a',href=True) if 'q=' in paper['href'] and '%' not in paper['href']]
            new_papers = new_papers[2:-1]

            for i in range(len(new_papers)):
                code = new_papers[i].split("/")[-1].split("?")[0]
                key = f"{names[i]}-{code}"
                value = f"https://www.pressarchive.cy{new_papers[i]}"
                self.newspaper_dictionary[key] = value

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            os.mkdir(newspaper)
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            pages = self.driver.find_element(By.CLASS_NAME, 'page-count')
            page_count = int(pages.text.replace("of ", ""))
            tuples = []
            for i in range(1,1+1):
                site = f"https://www.pressarchive.cy/s/en/item/31197?q=&page={i}"
                self.driver.get(site)
                soup = BeautifulSoup(self.driver.page_source,'lxml')
                new_dates = [date.text.split(" ")[1] for date in soup.find_all('h5') if '\n' not in date.text]
                new_links = [link['href'] for link in soup.find_all('a',href=True) if '/s/en/item/' in link['href'] and "#" not in link['href']]
                for i in range(len(new_links)):
                    tpl = f"https://www.pressarchive.cy{new_links[i]}",new_dates[i]
                    tuples.append(tpl)

            for tpl in tuples:
                link = tpl[0]
                date = tpl[1]
                self.driver.get(url=link)
                time.sleep(5)
                image = self.driver.find_element(By.ID,'thumb0')
                code = image.get_attribute('data-src')
                code = code.split("_")[1]
                pdf_link = f'https://www.pressarchive.cy/files/v2/publication_{code}_1/fullpdf'
                filename = f"{newspaper} {date}.pdf"
                response = requests.get(url=pdf_link)
                if response.status_code == 200:
                    with open(f"{newspaper}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{newspaper}/{filename} was downloaded.\n")
                    print(f"{newspaper}/{filename} was downloaded")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{newspaper}/{filename} was downloaded,it had response {response.status_code}\n")
                    print(f"{newspaper}/{filename} was downloaded,it had response {response.status_code}")





    # The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    # This method will check if all the newspapers have been downloaded or not
    def check_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            pages = self.driver.find_element(By.CLASS_NAME, 'page-count')
            page_count = int(pages.text.replace("of ", ""))
            tuples = []
            for i in range(1, 1 + 1):
                site = f"https://www.pressarchive.cy/s/en/item/31197?q=&page={i}"
                self.driver.get(site)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                new_dates = [date.text.split(" ")[1] for date in soup.find_all('h5') if '\n' not in date.text]
                new_links = [link['href'] for link in soup.find_all('a', href=True) if '/s/en/item/' in link['href'] and "#" not in link['href']]
                for i in range(len(new_links)):
                    tpl = f"https://www.pressarchive.cy{new_links[i]}", new_dates[i]
                    tuples.append(tpl)

            for tpl in tuples:
                link = tpl[0]
                date = tpl[1]
                self.driver.get(url=link)
                time.sleep(5)
                image = self.driver.find_element(By.ID, 'thumb0')
                code = image.get_attribute('data-src')
                code = code.split("_")[1]
                pdf_link = f'https://www.pressarchive.cy/files/v2/publication_{code}_1/fullpdf'
                filename = f"{newspaper} {date}.pdf"
                if filename not in os.listdir(newspaper):
                    response = requests.get(url=pdf_link)
                    if response.status_code == 200:
                        with open(f"{newspaper}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{newspaper}/{filename} was downloaded.\n")
                        print(f"{newspaper}/{filename} was downloaded")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{newspaper}/{filename} was downloaded,it had response {response.status_code}\n")
                        print(f"{newspaper}/{filename} was downloaded,it had response {response.status_code}")

    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

    # This method will print the names/codes of all the newspapers
    def print_newspaper_names(self):
        for newspaper in self.newspaper_dictionary:
            print(newspaper)

if __name__ == "__main__":
    cpio = CyprusPressInformationOffice()
    cpio.check_newspapers()
