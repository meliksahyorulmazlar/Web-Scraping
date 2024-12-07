#Webscraper to download the front page of Argentinian newspaper Clarin from day a to day b where a is later than day b
import datetime,requests,lxml,time
from bs4 import BeautifulSoup


class Clarin:
    def __init__(self,start_date,end_date):
        #datetime.datetime(month=6,day=8,year=2024)
        self.start_date = start_date
        self.one_day = datetime.timedelta(days=1)
        self.end_date = end_date
        self.end_date += self.one_day

    #the start date should be later than the end date
    def download(self):
        try:
            os.makedirs("Clarin Headlines")
        except FileExistsError:
            pass
        while self.start_date != self.end_date:
            year = self.start_date.year
            month = self.start_date.strftime("%m")
            day = self.start_date.strftime("%d")
            image = f"https://tapas.clarin.com/tapa/{year}/{month}/{day}/{year}{month}{day}_thumb.jpg"
            response = requests.get(url=image)
            if response.status_code == 200:
                photo = response.content
                with open(f"{day}-{month}-{year}.jpg","wb") as data_file:
                    data_file.write(photo)

                with open("download_results.txt","a") as data_file:
                    data_file.write(f"{day}/{month}/{year}.jpg was downloaded \n")
                print(f"{day}-{month}-{year}.jpg was downloaded \n")
                self.start_date += self.one_day

            elif response.status_code == 404:
                with open("download_results.txt","a") as data_file:
                    data_file.write(f"{day}/{month}/{year} does not exist\n")
                self.start_date += self.one_day

            else:
                print(self.start_date)
                break



if __name__ == "__main__":
    year_now = datetime.datetime.now().year
    month_now = datetime.datetime.now().month
    day_now = datetime.datetime.now().day
    #If you want to get all of the photos:
    #The earliest date is the 28th August 1945
    clarin = Clarin(start_date=datetime.datetime(day=28,month=8,year=1945),end_date=datetime.datetime(day=day_now,month=month_now,year=year_now))
    clarin.download()
