#Sabah front page webscraper
#Sabah is a famous newspaper in Turkey


import requests, os, lxml,datetime
from bs4 import BeautifulSoup


class Takvim:
    def __init__(self):
        self.start_date = datetime.datetime(day=11, month=8, year=2010)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    #This method will return today's date
    def return_today(self)->datetime.datetime:
        today = datetime.datetime.today()
        return datetime.datetime(day=today.day, month=today.month, year=today.year)

    #This method will download any date between the 11th August 2010 and today
    def download_date(self, date: datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            website = f"https://egazete.sabah.com.tr/eGazete/image/www_sabah_com_tr/{year}/{month}/{day}/1"
            formatted_date = f"{day}-{month}-{year}"
            
            response = requests.get(url=website)


            if len(response.content) >100:
                if response.status_code == 200:
                    with open(f"{formatted_date}.jpeg", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{formatted_date} was downloaded\n")
                    print(f"{formatted_date} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{formatted_date} was not on the archive, it was only {len(response.content)} bytes\n")
                print(f"{formatted_date} was not on the archive, it was only {len(response.content)} bytes")

    #This method will download all the dates from d1 till d2
    #For example,download_d1_d2(d1=datetime.datetime(day=10,month=1,year=2011),d2=datetime.datetime(day=13,month=2,year=2011))
    #will download the front pages of the following days:
    #10th,11th,12th,13th January 2011
    def download_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    #This method will download of Sabah's front page archive from the 11th august 2010 till today
    def download_all(self):
        self.download_d1_d2(self.start_date, self.today)

    #This method will download today's front page of Sabah
    def download_today(self):
        self.download_date(date=self.today)

    # The following method will check a particular date to see if it has been downloaded or not
    def check_download(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            website = f"https://egazete.sabah.com.tr/eGazete/image/www_sabah_com_tr/{year}/{month}/{day}/1"
            formatted_date = f"{day}-{month}-{year}"

            if f"{formatted_date}.jpeg" not in os.listdir():
                response = requests.get(url=website)

                if len(response.content) > 100:
                    if response.status_code == 200:
                        with open(f"{formatted_date}.jpeg", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{formatted_date} was downloaded\n")
                        print(f"{formatted_date} was downloaded")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{formatted_date} was not on the archive, it was only {len(response.content)} bytes\n")
                    print(f"{formatted_date} was not on the archive, it was only {len(response.content)} bytes")

    # The following method will check from one date to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_download(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.start_date,self.today)



if __name__ == "__main__":
    takvim = Takvim()
    takvim.download_d1_d2(d1=datetime.datetime(day=3,month=10,year=2016),d2=takvim.today)
