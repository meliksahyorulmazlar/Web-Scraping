#Olay Gazetesi front page webscraper


import requests,os,lxml,datetime
from bs4 import BeautifulSoup



class OlayGazetesi:
    def __init__(self):
        self.first = datetime.datetime(day=1,month=1,year=2008)
        self.today = self.get_today()
        self.one_day = datetime.timedelta(days=1)

    #This will return today's date
    def get_today(self):
        date = datetime.datetime.now()
        return datetime.datetime(day=date.day,month=date.month,year=date.year)

    def download_date(self,date:datetime.datetime):
        if self.first <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{year}-{month}-{day}"
            website = f"https://e-gazete.olay.com.tr/olay-gazetesi/date/{formatted_date}"

            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            images = [link["href"] for link in soup.find_all("a",href=True) if "image" in link["href"]]
            if len(images) == 0:
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} had nothing\n")
                print(f"{formatted_date} had nothing")
            else:
                os.makedirs(f"{formatted_date}")
                for i in range(len(images)):
                    filename = f"{formatted_date}-{i}.jpg"

                    response = requests.get(url=images[i])

                    if response.status_code == 200:
                        with open(f"{formatted_date}/{filename}","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{formatted_date} was downloaded\n")
                        print(f"{formatted_date} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")



    #This method will download today's front page of Olay Gazete
    def download_today(self):
        self.download_date(self.today)


    #This method will download from one date to another
    #download_d1_d2(datetime.datetime(day=1,month=1,year=2008),datetime.datetime(day=5,month=1,year=2008))
    #will end up downloading 1st,2nd,3rd,4th,5th January 2005
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    #The method will download the entire Olay Gazete archive
    def download_all(self):
        self.download_d1_d2(self.first,self.today)

    # The following method will check a particular date to see if it has been downloaded onot
    def check(self,date:datetime.datetime):
        if self.first <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{year}-{month}-{day}"
            website = f"https://e-gazete.olay.com.tr/olay-gazetesi/date/{formatted_date}"

            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            images = [link["href"] for link in soup.find_all("a", href=True) if "image" in link["href"]]
            if len(images) == 0:
                with open("download_results.txt", "a") as f:
                    f.write(f"{formatted_date} had nothing\n")
                print(f"{formatted_date} had nothing")
            else:
                os.makedirs(f"{formatted_date}")
                for i in range(len(images)):
                    filename = f"{formatted_date}-{i}.jpg"
                    if filename not in os.listdir(formatted_date):
                        response = requests.get(url=images[i])
                        if response.status_code == 200:
                            with open(f"{formatted_date}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{formatted_date} was downloaded\n")
                            print(f"{formatted_date} was downloaded")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(
                                    f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")

    # The following method will check the newspapers from one date to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.first,self.today)

if __name__ == "__main__":
    og = OlayGazetesi()
    #og.download_d1_d2(datetime.datetime(day=1,month=1,year=2008),datetime.datetime(day=5,month=1,year=2008))
    og.download_all()


