#Kayhan pdf webscraper
#Kayhan is a famous newspaper in Iran
#Kayhan in Persian/Farsi means universe
#This is the English version of Kayhan

import persiantools.jdatetime
from persiantools.jdatetime import JalaliDate
import requests,os,lxml
from bs4 import BeautifulSoup
from datetime import timedelta,datetime


class KayhanEnglish:
    def __init__(self):
        current_day = datetime.today().day
        current_month = datetime.today().month
        current_year = datetime.today().year
        self.webpage = "https://kayhan.ir"
        #This is the first date found on the archive
        self.first_day = datetime(day=8,month=5,year=2014)
        self.today = datetime(day=current_day,month=current_month,year=current_year)

    #This will download a date
    def download_date(self,current_date):
        formatted_date = current_date.strftime('%Y/%m/%d')
        webpage_url = f"https://kayhan.ir/en/publication?type_id=*&publication_id=-1&rpp=5&from_date={formatted_date}&to_date={formatted_date}&p=1"
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
            os.makedirs(directory_name)
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

    #The method will download all of Kayhan's English online archive
    def download_all(self):
        self.download_dates(self.first_day,self.today)

    #The method will download today's paper of Kayhan English
    def download_today(self):
        self.download_date(current_date=self.today)

    #If you would like to input the dates in the gregorian calendar, you can use this method instead
    #kf.download_dates(datetime(day=4,month=2,year=2024),datetime(day=6,month=2,year=2024))
    #This will download all the newspapers for:
    #4th,5th,6th February 2024
    def download_dates(self,d1:datetime,d2:datetime):
        if d1 > d2:
            day = d2
            d2 = d1
            d1 = day
        current_date = d1
        while current_date <= d2:
            self.download_date(current_date)
            current_date += timedelta(days=1)

if __name__ == "__main__":
    ke = KayhanEnglish()
    ke.download_all()



