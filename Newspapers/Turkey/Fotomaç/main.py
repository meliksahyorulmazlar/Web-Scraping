#Fotomaç Front page webscraper
#Fotomaç is a famous Turkish sports Newspaper


import requests,os,lxml,datetime
from bs4 import BeautifulSoup



class Fotomac:
    def __init__(self):
        self.start_date = datetime.datetime(day=1,month=1,year=2021)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    #This method will return today's date
    def return_today(self)->datetime.datetime:
        today = datetime.datetime.today()
        return datetime.datetime(day=today.day, month=today.month, year=today.year)

    #This method will download any date between the 1st January 2021 and today
    def download_date(self, date: datetime.datetime):
        if date < self.start_date or date > self.today:
            print("The date is not on the archive or the date is in the future.")
        else:

            day = date.day
            month = date.month
            year = date.year
            website = f"https://egazete.fotomac.com.tr/eGazete/image/www_fotomac_com_tr/{year}/{month}/{day}/1"

            response = requests.get(url=website)

            formatted_date = f"{day}-{month}-{year}"
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

    #This method will download all the dates from d1 till d2
    #For example,download_d1_d2(d1=datetime.datetime(day=10,month=1,year=2021),d2=datetime.datetime(day=13,month=2,year=2021))
    #will download the front pages of the following days:
    #10th,11th,12th,13th January 2021
    def download_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    #This method will download of Fotomaç's front page archive from the 1st January 2021 till today
    def download_all(self):
        self.download_d1_d2(self.start_date, self.today)

    #This method will download today's front page of Takvim
    def download_today(self):
        self.download_date(date=self.today)




if __name__ == "__main__":
    fotomac = Fotomac()
    fotomac.download_all()