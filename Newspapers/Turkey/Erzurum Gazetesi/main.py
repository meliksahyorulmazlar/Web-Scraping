#Erzurum Gazetesi pdf webscraper
#Erzurum Gazetesi is a newspaper about the latest developments in Erzurum, a province of Turkey


import requests,os,lxml,datetime
from bs4 import BeautifulSoup


class ErzurumGazetesi:
    def __init__(self):
        self.first = datetime.datetime(day=27,month=10,year=2014)
        self.today = self.today()
        self.one_day = datetime.timedelta(days=1)
        self.main = "http://www.erzurumgazetesi.com.tr"

    #This method will return today's date
    def today(self)->datetime.datetime:
        today = datetime.datetime.now()
        return datetime.datetime(day=today.day,month=today.month,year=today.year)

    #Method to download a date
    def download_date(self,date:datetime.datetime):
        if self.first <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            page = f"http://www.erzurumgazetesi.com.tr/default.asp?page=arsiv&gun={day}&ay={month}&yil={year}&ge=Getir"
            soup = BeautifulSoup(requests.get(url=page).text,"lxml")

            links = [f"{self.main}{link['href']}" for link in soup.find_all("a",href=True,class_="fancybo")]
            formatted_date = f"{day}-{month}-{year}"
            if len(links) == 0:
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} had no links on the archive\n")
                print(f"{formatted_date} had no links on the archive")
            else:
                os.makedirs(formatted_date)
                for link in links:
                    print(link)
                    response = requests.get(url=link)
                    filename = link.split("/")[-1]
                    if response.status_code == 200:
                        with open(f"{formatted_date}/{filename}","wb") as f:
                            f.write(response.content)
                        with open(f"download_results.txt","a") as f:
                            f.write(f"{formatted_date}/{filename} was downloaded\n")
                        print(f"{formatted_date}/{filename} was downloaded")
                    else:
                        with open(f"download_results.txt","a") as f:
                            f.write(f"{formatted_date}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{formatted_date}/{filename} was not downloaded,it had response status code {response.status_code}")

    #This method will download all the newspapers from one date till another date
    #download_d1_d2(d1=datetime.datetime(day=27,month=10,year=2014),d2=datetime.datetime(day=27,month=11,year=2014))
    #The method will download all the newspapers from the 27th October 2014 till 27th November 2014
    #It will download 27th November too
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c
        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    #This method will download all the archive
    def download_all(self):
        self.download_d1_d2(self.first,self.today)


if __name__ == "__main__":
    eg = ErzurumGazetesi()
    eg.download_all()
