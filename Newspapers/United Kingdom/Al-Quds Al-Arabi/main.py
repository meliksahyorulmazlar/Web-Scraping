#Al-Quds Al-Arabi, an arabic newspaper headquartered in London
import datetime
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
class AlQudsAlArabi:
    def __init__(self):
        self.start_date = datetime.datetime(day=14,month=1,year=1998)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)
        self.start_webdriver()


    # The following method will return today's date
    def return_today(self)->datetime.datetime:
        t = datetime.datetime.now()
        day = t.day
        month = t.month
        year = t.year
        return datetime.datetime(day=day,month=month,year=year)

    # The following method will start the selenium webdriver
    def start_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=options)

    # The following method will download a specific date:
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            website = f"https://pdf.alquds.co.uk/index.php/{year}/{month}/{day}/"
            self.driver.get(website)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            pdf = soup.find('a',href=True,class_='pdf-download')
            print(pdf)
            if pdf is None:
                print(f"{day}-{month}-{year} had no pdf")
            else:
                pdf = 'https:'+ pdf['href']
                filename = f"{day}-{month}-{year}.pdf"
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}.")

    # The following method will download from one date to another later date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(date=d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.today)

    # The following method will check a specific date:
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            filename = f"{day}-{month}-{year}.pdf"
            if filename not in os.listdir():
                website = f"https://pdf.alquds.co.uk/index.php/{year}/{month}/{day}/"
                self.driver.get(website)
                soup = BeautifulSoup(self.driver.page_source,'lxml')
                pdf = soup.find('a',href=True,class_='pdf-download')
                print(pdf)
                if pdf is None:
                    print(f"{day}-{month}-{year} had no pdf")
                else:
                    pdf = 'https:'+ pdf['href']
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}.")
            else:
                print(f"{filename} was already downloaded")

    # The following method will check from one date to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(date=d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(d1=self.start_date,d2=self.today)


if __name__ == "__main__":
    alquds_alarabi = AlQudsAlArabi()
    alquds_alarabi.download_all()
