# Al-Ayyam, Palestinian Newspaper
import datetime

import requests,os,lxml
from bs4 import BeautifulSoup

class AlAyyam:
    def __init__(self):
        self.start_date = datetime.datetime(day=1,month=1,year=2005)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    # The following method will return today's date
    def return_today(self)->datetime.datetime:
        t = datetime.datetime.now()
        day = t.day
        month = t.month
        year = t.year
        return datetime.datetime(day=day,month=month,year=year)

    # The following method will download a particular date
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            main_directory = f"{day}-{month}-{year}"
            os.mkdir(main_directory)
            website = f'https://www.al-ayyam.ps/ar/PDF?f_sub=f_sub&day_op={day}&month_op={month}&year_op={year}'
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            pdfs = []
            for pdf in soup.find_all('a',href=True,target=True):
                if '.pdf' in pdf['href']:
                    if pdf['href'] not in pdfs:
                        pdfs.append(pdf['href'])

            for pdf in pdfs:
                response = requests.get(pdf)
                filename = pdf.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{main_directory}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{main_directory}/{filename} was downloaded.\n")
                    print(f"{main_directory}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{main_directory}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{main_directory}/{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one date to another later date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day


    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.today)

    # The following method will check a particular date
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            main_directory = f"{day}-{month}-{year}"
            try:
                os.mkdir(main_directory)
            except FileExistsError:
                pass
            website = f'https://www.al-ayyam.ps/ar/PDF?f_sub=f_sub&day_op={day}&month_op={month}&year_op={year}'
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            pdfs = []
            for pdf in soup.find_all('a',href=True,target=True):
                if '.pdf' in pdf['href']:
                    if pdf['href'] not in pdfs:
                        pdfs.append(pdf['href'])

            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(f"{main_directory}"):
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{main_directory}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{main_directory}/{filename} was downloaded.\n")
                        print(f"{main_directory}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{main_directory}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{main_directory}/{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{main_directory}/{filename} was already downloaded")

    # The following method will download from one date to another later date
    def check_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def check_all(self):
        self.check_d1_d2(d1=self.start_date, d2=self.today)

if __name__ == "__main__":
    alayyam = AlAyyam()
    alayyam.check_date(date=alayyam.today)