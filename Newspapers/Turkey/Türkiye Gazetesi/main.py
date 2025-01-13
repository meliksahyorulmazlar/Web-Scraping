#Türkiye Gazetesi Front page webscraper
#Türkiye Gazetesi is a famous Turkish newspaper
import os

import requests,lxml,datetime
from bs4 import BeautifulSoup


class TurkiyeGazetesi:
    def __init__(self):
        self.start_date = datetime.datetime(day=1,month=1,year=2016)
        self.today = self.get_today()
        self.one_day = datetime.timedelta(days=1)

    #This method will return today's date
    def get_today(self)->datetime.datetime:
        today = datetime.datetime.today()
        day = today.day
        month = today.month
        year = today.year
        return datetime.datetime(day=day,month=month,year=year)

    #This method will download any date between the 1st January 2016 and today
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{day}-{month}-{year}"
            if month < 10:
                month = f"0{month}"

            if day < 10:
                day = f"0{day}"

            website = f"https://uye.turkiyegazetesi.com.tr/index/cover?date={year}-{month}-{day}"

            response = requests.get(url=website)

            if response.status_code == 200:
                with open(f"{formatted_date}.pdf","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} was downloaded\n")
                print(f"{formatted_date} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")


    #This method will download all the dates from one date to another
    #The following example:
    #download_d1_d2(d1=datetime.datetime(day=1,month=1,year=2016),d2=datetime.datetime(day=5,month=1,year=2016))
    #will download the following dates:
    #1st,2nd,3rd,4th,5th January 2016


    def download_d1_d2(self,d1:datetime.datetime,d2=datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    #This method will download all the dates from the 1st January 2016 till today
    #or in other words it will download the entire archive of the newspaper
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.today)

    #This method will download today's front page of Türkiye Gazetesi
    def download_today(self):
        self.download_date(date=self.today)

    # The following method will check if the particular got downloaded or not
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{day}-{month}-{year}"
            if month < 10:
                month = f"0{month}"

            if day < 10:
                day = f"0{day}"

            website = f"https://uye.turkiyegazetesi.com.tr/index/cover?date={year}-{month}-{day}"

            if f"{formatted_date}.pdf" not in os.listdir():
                response = requests.get(url=website)
                if response.status_code == 200:
                    with open(f"{formatted_date}.pdf","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{formatted_date} was downloaded\n")
                    print(f"{formatted_date} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")

    #The following method will check from one to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.start_date,self.today)


if __name__ == "__main__":
    tg = TurkiyeGazetesi()
    tg.download_all()
