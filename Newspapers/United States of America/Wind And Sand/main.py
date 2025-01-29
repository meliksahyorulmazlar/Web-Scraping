# Wind And Sand Webscraper


from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,time,os
from bs4 import BeautifulSoup

class WindAndSand:
    def __init__(self):
        self.start_webdriver()
        self.minimum_date = (1,1950)
        self.maximum_date = (12,2021)


    # The following method will start the webdriver
    def start_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url='https://www.wsmrhistoric.com/Search/Date#')

    # The following method will find the xpath of the date
    def find_x_path(self,date:tuple):
        month = date[0]
        year = date[1]-1949
        return f'/html/body/div[2]/div[1]/ul[{year}]/li[{month}]/a '

    # The following method will download the dates
    def download_date(self,date:tuple):
        if self.driver.current_url != 'https://www.wsmrhistoric.com/Search/Date#':
            self.driver.get('https://www.wsmrhistoric.com/Search/Date#')
        try:
            os.mkdir('Dates')
        except FileExistsError:
            pass
        path = self.find_x_path(date)
        x = self.driver.find_element(By.XPATH, path)
        time.sleep(1)
        x.click()
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if
                '.pdf' in pdf['href'] and 'lowres' not in pdf['href']]
        for pdf in pdfs:
            website = f"https://www.wsmrhistoric.com{pdf}"
            filename = pdf.split('/')[-1].replace("#search=", '')
            response = requests.get(website)
            if response.status_code == 200:
                with open(f"Dates/{filename}", 'wb') as f:
                    f.write(response.content)
                with open('download_results.txt', 'a') as f:
                    f.write(f"{filename} was downloaded.\n")
                print(f"{filename} was downloaded.")
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(
                        f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will download all the dates from one date to another date
    def download_d1_d2(self,d1:tuple,d2:tuple):
        d1,d2 = self.compare(d1, d2)

        while d1 != d2:
            print(d1)
            self.download_date(d1)
            if d1[0] == 12:
                x = 1
                y = d1[1] + 1
                d1 = x,y
            else:
                x = d1[0]+1
                y = d1[1]
                d1 = x,y
        if d1 == d2:
            print(d1)
            self.download_date(d1)

    # The following method will check if all the pdfs for a specific date were downloaded or not.If they were not downloaded, they will get downloaded
    def check_date(self,date:tuple):
        if self.driver.current_url != 'https://www.wsmrhistoric.com/Search/Date#':
            self.driver.get('https://www.wsmrhistoric.com/Search/Date#')
        try:
            os.mkdir('Dates')
        except FileExistsError:
            pass
        path = self.find_x_path(date)
        x = self.driver.find_element(By.XPATH, path)
        time.sleep(1)
        x.click()
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if
                '.pdf' in pdf['href'] and 'lowres' not in pdf['href']]
        for pdf in pdfs:
            website = f"https://www.wsmrhistoric.com{pdf}"
            filename = pdf.split('/')[-1].replace("#search=", '')
            if filename not in os.listdir():
                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"Dates/{filename}", 'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(
                            f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")
            else:
                print(f"{filename} was already downloaded")

    # The following method will download all the dates
    def download_all(self):
        self.download_d1_d2(d1=self.minimum_date,d2=self.maximum_date)

    # The following method will check all the dates
    def check_all(self):
        self.check_d1_d2(d1=self.minimum_date,d2=self.maximum_date)

    # The following method will download all the supplements
    def download_supplements(self):
        self.driver.get(url='https://www.wsmrhistoric.com/Ads')
        os.mkdir('Supplements')
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href'] and 'lowres' not in pdf['href']]
        for pdf in pdfs:
            website = f"https://www.wsmrhistoric.com{pdf}"
            filename = pdf.split('/')[-1].replace("#search=", '')
            response = requests.get(website)
            if response.status_code == 200:
                with open(f"Supplements/{filename}", 'wb') as f:
                    f.write(response.content)
                with open('download_results.txt', 'a') as f:
                    f.write(f"{filename} was downloaded.\n")
                print(f"{filename} was downloaded.")
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will check all the supplements to see if they have been downloaded or not
    def check_supplements(self):
        self.driver.get(url='https://www.wsmrhistoric.com/Ads')
        try:
            os.mkdir('Supplements')
        except FileExistsError:
            pass
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if
                '.pdf' in pdf['href'] and 'lowres' not in pdf['href']]
        for pdf in pdfs:
            website = f"https://www.wsmrhistoric.com{pdf}"
            filename = pdf.split('/')[-1].replace("#search=", '')
            if filename not in os.listdir('Supplements'):
                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"Supplements/{filename}", 'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")
            else:
                print(f"{filename} was already downloaded")

    # The following method will get the right d1 and d2
    def compare(self,d1:tuple,d2:tuple):
        if d1[1] < 1950:
            d1 = self.minimum_date

        if d2[1] < 1950:
            d2 = self.minimum_date

        if d2[1] > 2021:
            d2 = self.maximum_date

        if d1[1] > 2021:
            d1 = self.maximum_date

        if d1[0] > 12:
            x = 12
            y = d1[1]
            d1 = x,y

        if d2[0] > 12:
            x = 12
            y = d2[1]
            d1 = x,y

        if d1[1] > d2[1]:
            return d2,d1

        if d1[1] < d2[1]:
            return d1,d2

        if d1[0] > d2[0]:
            return d2,d1

        return d1,d2

    # The following method will check from one date to another later date
    def check_d1_d2(self,d1:tuple,d2:tuple):
        d1,d2 = self.compare(d1,d2)
        while d1 != d2:
            print(d1)
            self.check_date(d1)
            if d1[0] == 12:
                x = 1
                y = d1[1] + 1
                d1 = x,y
            else:
                x = d1[0]+1
                y = d1[1]
                d1 = x,y
        if d1 == d2:
            print(d1)
            self.check_date(d1)

if __name__ == '__main__':
    windsand = WindAndSand()
    windsand.check_d1_d2(d1=(1,2024),d2=(1,2023))
