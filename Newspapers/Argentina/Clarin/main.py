#Webscraper to download the front page of Argentinian newspaper Clarin from day a to day b where a is later than day b
import datetime,requests,lxml,time
import os

from bs4 import BeautifulSoup


class Clarin:
    def __init__(self):
        #datetime.datetime(month=6,day=8,year=2024)
        self.start_date = datetime.datetime(day=28, month=8, year=1945)
        self.one_day = datetime.timedelta(days=1)
        year_now = datetime.datetime.now().year
        month_now = datetime.datetime.now().month
        day_now = datetime.datetime.now().day
        self.end_date = datetime.datetime(day=day_now, month=month_now, year=year_now)
        # self.end_date += self.one_day
        # If you want to get all the photos:
        # The earliest date is the 28th August 1945

    #The following method will download the headline for a  particular date
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.end_date:
            year = self.start_date.year
            month = self.start_date.strftime("%m")
            day = self.start_date.strftime("%d")
            image = f"https://tapas.clarin.com/tapa/{year}/{month}/{day}/{year}{month}{day}_thumb.jpg"
            response = requests.get(url=image)
            if response.status_code == 200:
                photo = response.content
                with open(f"{day}-{month}-{year}.jpg", "wb") as data_file:
                    data_file.write(photo)

                with open("download_results.txt", "a") as data_file:
                    data_file.write(f"{day}/{month}/{year}.jpg was downloaded \n")
                print(f"{day}-{month}-{year}.jpg was downloaded \n")
                self.start_date += self.one_day

            elif response.status_code == 404:
                with open("download_results.txt", "a") as data_file:
                    data_file.write(f"{day}/{month}/{year} does not exist\n")
                self.start_date += self.one_day
            else:
                print(self.start_date)

    #This method will download from one date to another
    def download_d1_d2(self,date1:datetime.datetime,date2:datetime.datetime):
        if date1 > date2:
            c = date1
            date1 = date2
            date2 = c
        while date1 <= date2:
            self.download_date(date1)
            date1 += self.one_day

    #The following method will download all the headlines
    def download_all(self):
        start = self.start_date
        end = self.end_date
        self.download_d1_d2(start,end)

    #This method will check if the headline for a particular date got downloaded or not
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.end_date:
            year = self.start_date.year
            month = self.start_date.strftime("%m")
            day = self.start_date.strftime("%d")
            image = f"https://tapas.clarin.com/tapa/{year}/{month}/{day}/{year}{month}{day}_thumb.jpg"
            if f"{day}-{month}-{year}.jpg" not in os.listdir():
                response = requests.get(url=image)
                if response.status_code == 200:
                    photo = response.content
                    with open(f"{day}-{month}-{year}.jpg", "wb") as data_file:
                        data_file.write(photo)

                    with open("download_results.txt", "a") as data_file:
                        data_file.write(f"{day}/{month}/{year}.jpg was downloaded \n")
                    print(f"{day}-{month}-{year}.jpg was downloaded \n")
                    self.start_date += self.one_day

                elif response.status_code == 404:
                    with open("download_results.txt", "a") as data_file:
                        data_file.write(f"{day}/{month}/{year} does not exist\n")
                    self.start_date += self.one_day
                else:
                    print(self.start_date)

    #The following method will check if the headlines from one date to another date has been downloaded or not
    def check_d1_d2(self,date1:datetime.datetime,date2:datetime.datetime):
        if date1 > date2:
            c = date1
            date1 = date2
            date2 = c
        while date1 <= date2:
            self.check_date(date1)
            date1 += self.one_day

    # The following method will check if all the headlines have been downloaded or not
    def check_all(self):
        start = self.start_date
        end = self.end_date
        self.download_d1_d2(start,end)


if __name__ == "__main__":
    clarin.download()
