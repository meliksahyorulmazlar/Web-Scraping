# Denmark Library


import requests,os,lxml,time,datetime,shutil
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class DenmarkLibrary:
    def __init__(self):
        self.newspapers = {}
        self.start_webdriver()
        self.current_year = datetime.datetime.now().year
        self.gather_newspapers()


    # The following method will start the selenium webdriver
    def start_webdriver(self)->None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method will gather all the newspapers on the archive
    def gather_newspapers(self)->None:
        self.driver.get('https://www2.statsbiblioteket.dk/mediestream/avis/list')
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME,'newspaper')
            except selenium.common.exceptions.NoSuchElementException:
                pass
            else:
                break

        soup = BeautifulSoup(self.driver.page_source,'lxml')
        newspapers = [(n.text,f"https://www2.statsbiblioteket.dk/mediestream/avis/{n['href']}") for n in soup.find_all('a',href=True,class_='newspaper')]
        for n in newspapers:
            self.newspapers[n[0]] = n[1]

    # The following method will print the names of all the newspapers
    def print_names(self):
        for n in self.newspapers:
            print(n)

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            os.mkdir(newspaper)
            website = self.newspapers[newspaper]
            self.driver.get(website)

            while True:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "a[data-year]")
                except selenium.common.exceptions.NoSuchElementException:
                    self.driver.execute_script("window.scrollBy(0, 1000);")
                else:
                    break

            year_soup = BeautifulSoup(self.driver.page_source, 'lxml')
            new_years = [int(year['data-year']) for year in year_soup.find_all('a',attrs={'data-year':True}) ]
            years = []
            for year in new_years:
                if self.current_year-year >= 100:
                    years.append(year)
            print(years)
            if not years:
                print(f"The newspaper need to be older-(at least 100 years old)")
                shutil.rmtree(newspaper)
            else:
                for year in years:
                    year_website = f"{website}/{year}"
                    self.driver.get(year_website)
                    while True:
                        try:
                            self.driver.find_element(By.CLASS_NAME, 'query')
                        except selenium.common.exceptions.NoSuchElementException:
                            pass
                        else:
                            break
                    year_soup = BeautifulSoup(self.driver.page_source,'lxml')
                    new_dates = [f"https://www2.statsbiblioteket.dk{date['href']}" for date in year_soup.find_all('a',class_='query') ]
                    for date in new_dates:
                        dt = date.split("iso_dateTime:")
                        filename = dt[1][0:10:]
                        self.driver.get(date)

                        while True:
                            try:
                                final_link = self.driver.find_element(By.CLASS_NAME,'record')
                            except selenium.common.exceptions.NoSuchElementException:
                                pass
                            else:
                                break


                        self.driver.get(final_link.get_attribute('href'))
                        while True:
                            try:
                                pdf_link = self.driver.find_element(By.CLASS_NAME,'downloadPaperPDF')
                            except selenium.common.exceptions.NoSuchElementException:
                                pass
                            else:
                                print(pdf_link.get_attribute('href'))
                                break

                        response = requests.get(pdf_link.get_attribute('href'))
                        if response.status_code == 200:
                            with open(f"{newspaper}/{filename}.pdf",'wb') as f:
                                f.write(response.content)
                            with open(f"download_results.txt",'a') as f:
                                f.write(f"{newspaper}/{filename}.pdf was downloaded.\n")
                            print(f"{newspaper}/{filename}.pdf was downloaded.")
                        else:
                            with open(f"download_results.txt",'a') as f:
                                f.write(f"{newspaper}/{filename}.pdf was not downloaded, it had response status code {response.status_code}\n")
                            print(f"{newspaper}/{filename}.pdf was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspapers:
            self.download_newspaper(newspaper)

    # The following method will check a specific newspaper
    def check_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            website = self.newspapers[newspaper]
            self.driver.get(website)

            while True:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "a[data-year]")
                except selenium.common.exceptions.NoSuchElementException:
                    self.driver.execute_script("window.scrollBy(0, 1000);")
                else:
                    break

            year_soup = BeautifulSoup(self.driver.page_source, 'lxml')
            new_years = [int(year['data-year']) for year in year_soup.find_all('a', attrs={'data-year': True})]
            years = []
            for year in new_years:
                if self.current_year - year >= 100:
                    years.append(year)
            print(years)
            if not years:
                print(f"The newspaper need to be older-(at least 100 years old)")
                shutil.rmtree(newspaper)
            else:
                for year in years:
                    year_website = f"{website}/{year}"
                    self.driver.get(year_website)
                    while True:
                        try:
                            self.driver.find_element(By.CLASS_NAME, 'query')
                        except selenium.common.exceptions.NoSuchElementException:
                            pass
                        else:
                            break
                    year_soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    new_dates = [f"https://www2.statsbiblioteket.dk{date['href']}" for date in
                                 year_soup.find_all('a', class_='query')]
                    for date in new_dates:
                        dt = date.split("iso_dateTime:")
                        filename = dt[1][0:10:]
                        if f"{filename}.pdf" not in os.listdir(f"{newspaper}"):
                            self.driver.get(date)

                            while True:
                                try:
                                    final_link = self.driver.find_element(By.CLASS_NAME, 'record')
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass
                                else:
                                    break

                            self.driver.get(final_link.get_attribute('href'))
                            while True:
                                try:
                                    pdf_link = self.driver.find_element(By.CLASS_NAME, 'downloadPaperPDF')
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass
                                else:
                                    print(pdf_link.get_attribute('href'))
                                    break

                            response = requests.get(pdf_link.get_attribute('href'))
                            if response.status_code == 200:
                                with open(f"{newspaper}/{filename}.pdf", 'wb') as f:
                                    f.write(response.content)
                                with open(f"download_results.txt", 'a') as f:
                                    f.write(f"{newspaper}/{filename}.pdf was downloaded.\n")
                                print(f"{newspaper}/{filename}.pdf was downloaded.")
                            else:
                                with open(f"download_results.txt", 'a') as f:
                                    f.write(f"{newspaper}/{filename}.pdf was not downloaded, it had response status code {response.status_code}\n")
                                print(f"{newspaper}/{filename}.pdf was not downloaded, it had response status code {response.status_code}")

    # The following method will check all the newspapers on the archive
    def check_all(self):
        for newspaper in self.newspapers:
            self.check_newspaper(newspaper)

if __name__ == "__main__":
    denmark_library = DenmarkLibrary()
    denmark_library.download_newspaper('Aalborg Tidende (1901-1904)')

