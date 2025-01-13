#Kayhan pdf webscraper
#Kayhan is a famous newspaper in Iran
#Kayhan in Persian/Farsi means universe

import persiantools.jdatetime
from persiantools.jdatetime import JalaliDate
import requests,os,lxml
from bs4 import BeautifulSoup
from datetime import timedelta,datetime


class Kayhan:
    def __init__(self):
        current_day = JalaliDate.today().day
        current_month = JalaliDate.today().month
        current_year = JalaliDate.today().year
        self.webpage = "https://kayhan.ir"
        #This is the first date found on the archive
        self.one_day = timedelta(days=1)
        self.first_day = JalaliDate(day=13,month=2,year=1394)
        self.today = JalaliDate(day=current_day,month=current_month,year=current_year)

    #This will download a date
    def download_date(self,current_date:persiantools.jdatetime.JalaliDate):
        if self.first_day <= current_date <= self.today:
            formatted_date = current_date.strftime('%Y/%m/%d')
            webpage_url = f"https://kayhan.ir/fa/publication?type_id=*&publication_id=-1&rpp=5&from_date={formatted_date}&to_date={formatted_date}&p=1"
            soup = BeautifulSoup(requests.get(url=webpage_url).text, "lxml")
            download_links = [f'{self.webpage}{link["href"]}' for link in soup.find_all("a", href=True) if ".pdf" in link["href"]]
            if len(download_links) == 0:
                pass
            else:
                day = current_date.day
                month = current_date.month
                year = current_date.year
                try:
                    os.makedirs(str(year))
                except FileExistsError:
                    pass
                directory_name = f"{year}/{day}-{month}-{year}"
                os.mkdir(directory_name)
                print(download_links)
                for download_link in download_links:
                    response = requests.get(url=download_link)
                    filename = download_link.split("/")[-1].split("?")[0]
                    saved_as = f"{directory_name}/{filename}"
                    result = f"{day}-{month}-{year} {filename}"
                    if response.status_code == 200:
                        with open(saved_as, "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{result} was downloaded\n")
                            print(f"{result} was downloaded")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(f"{result} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{result} was not downloaded,it had response status code {response.status_code}")

    #The method will download all of Kayhan's online archive
    def download_all(self):
        self.download_persian_dates(self.first_day,self.today)

    #The method will download today's paper of Kayhan
    def download_today(self):
        self.download_date(current_date=self.today)

    #kf.download_persian_dates(d1=JalaliDate(day=5,month=10,year=1398),d2=JalaliDate(day=9,month=10,year=1398))
    #This method will download all the newspapers for:
    #5th,6th,7th,8th,9th Dey 1398
    def download_persian_dates(self,d1:persiantools.jdatetime.JalaliDate,d2:persiantools.jdatetime.JalaliDate):
        current_date = d1
        while current_date <= d2:
            self.download_date(current_date)
            current_date += self.one_day

    #If you would like to input the dates in the gregorian calendar, you can use this method instead
    #kf.download_dates(datetime(day=4,month=2,year=2024),datetime(day=6,month=2,year=2024))
    #This will download all the newspapers for:
    #4th,5th,6th February 2025
    def download_dates(self,d1:datetime,d2:datetime):
        persian_date1 = JalaliDate.to_jalali(day=d1.day,month=d1.month,year=d1.year)
        persian_date2 = JalaliDate.to_jalali(day=d2.day, month=d2.month, year=d2.year)
        self.download_persian_dates(persian_date1,persian_date2)


    #The following method will check if a particular date got downloaded or not
    def check_download_date(self,current_date:persiantools.jdatetime.JalaliDate):
        if self.first_day <= current_date <= self.today:
            formatted_date = current_date.strftime('%Y/%m/%d')
            webpage_url = f"https://kayhan.ir/fa/publication?type_id=*&publication_id=-1&rpp=5&from_date={formatted_date}&to_date={formatted_date}&p=1"
            soup = BeautifulSoup(requests.get(url=webpage_url).text, "lxml")
            download_links = [f'{self.webpage}{link["href"]}' for link in soup.find_all("a", href=True) if
                              ".pdf" in link["href"]]
            if len(download_links) == 0:
                pass
            else:
                day = current_date.day
                month = current_date.month
                year = current_date.year
                try:
                    os.mkdir(str(year))
                except FileExistsError:
                    pass
                directory_name = f"{year}/{day}-{month}-{year}"
                try:
                    os.mkdir(directory_name)
                except FileExistsError:
                    pass
                print(download_links)
                for download_link in download_links:
                    filename = download_link.split("/")[-1].split("?")[0]
                    saved_as = f"{directory_name}/{filename}"
                    result = f"{day}-{month}-{year} {filename}"
                    if filename not in os.listdir(directory_name):
                        response = requests.get(url=download_link)
                        if response.status_code == 200:
                            with open(saved_as, "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{result} was downloaded\n")
                                print(f"{result} was downloaded")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"{result} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{result} was not downloaded,it had response status code {response.status_code}")

    #The following method will check from one date to another larger date
    def check_d1_d2(self,d1:persiantools.jdatetime.JalaliDate,d2:persiantools.jdatetime.JalaliDate):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_download_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.first_day,self.today)

if __name__ == "__main__":
    k = Kayhan()
