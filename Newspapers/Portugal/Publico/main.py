# Publico is a newspaper in Portugal

import datetime,requests
import os

from bs4 import BeautifulSoup



class Publico:
    def __init__(self):
        self.start_date = datetime.datetime(day=4,month=2,year=2001)
        self.today = self.find_today()
        self.one_day = datetime.timedelta(days=1)

    # The following method will today's date
    def find_today(self)->datetime.datetime:
        today = datetime.datetime.today()
        day = today.day
        month = today.month
        year = today.year
        return datetime.datetime(day=day,month=month,year=year)

    # This method downloads the front pages given the date
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"

            formatted_date1 = f"{year}{month}{day}"
            formatted_date2 = f"{year}/{month}/{day}"


            website = f"https://www.publico.pt/jornal?date={formatted_date1}"

            print(website)
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            print(formatted_date2)
            links = [image["data-media-viewer"] for image in soup.find_all("img",attrs={"data-media-viewer": True}) if formatted_date2 in image["data-media-viewer"]]
            if links:
                try:
                    os.mkdir(f"{date.year}")
                except FileExistsError:
                    pass

                formatted_date = f"{date.day}-{date.month}-{date.year}"

                os.mkdir(f"{date.year}/{formatted_date}")
                for link in links:
                    filename = link.split("/")[-1]
                    web_name = f"web{formatted_date1}"
                    filename = filename.replace("?tp=ARQUIVO","").replace(web_name,"")

                    response = requests.get(url=link)
                    if response.status_code == 200:
                        with open(f"{date.year}/{formatted_date}/{filename}","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{date.day}/{date.month}/{date.year} {filename} was downloaded\n")
                        print(f"{date.day}/{date.month}/{date.year} {filename} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{date.day}/{date.month}/{date.year} {filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{date.day}/{date.month}/{date.year} {filename} was not downloaded,it had response status code {response.status_code}")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{date.day}/{date.month}/{date.year} had no front pages\n")
                print(f"{date.day}/{date.month}/{date.year} had no front pages")


    #The following archive will download all the front pages from date d1 to date d2
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(date=d1)
            d1 += self.one_day

    # The following method will download the latest front pages from Publico
    def download_latest(self):
        self.download_date(date=self.today)

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.today)

    # The following method will check a particular date
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"

            formatted_date1 = f"{year}{month}{day}"
            formatted_date2 = f"{year}/{month}/{day}"

            website = f"https://www.publico.pt/jornal?date={formatted_date1}"

            print(website)
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            print(formatted_date2)
            links = [image["data-media-viewer"] for image in soup.find_all("img",attrs={"data-media-viewer": True}) if formatted_date2 in image["data-media-viewer"]]
            if links:
                try:
                    os.mkdir(f"{date.year}")
                except FileExistsError:
                    pass

                formatted_date = f"{date.day}-{date.month}-{date.year}"
                try:
                    os.mkdir(f"{date.year}/{formatted_date}")
                except FileExistsError:
                    pass

                for link in links:
                    filename = link.split("/")[-1]
                    web_name = f"web{formatted_date1}"
                    filename = filename.replace("?tp=ARQUIVO","").replace(web_name,"")
                    if filename not in os.listdir(f"{date.year}/{formatted_date}"):
                        response = requests.get(url=link)
                        if response.status_code == 200:
                            with open(f"{date.year}/{formatted_date}/{filename}","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{date.day}/{date.month}/{date.year} {filename} was downloaded\n")
                            print(f"{date.day}/{date.month}/{date.year} {filename} was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{date.day}/{date.month}/{date.year} {filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{date.day}/{date.month}/{date.year} {filename} was not downloaded,it had response status code {response.status_code}")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{date.day}/{date.month}/{date.year} had no front pages\n")
                print(f"{date.day}/{date.month}/{date.year} had no front pages")

    # The following method will check from one date to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # This methos will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.start_date,self.today)

if __name__ == "__main__":
    publico = Publico()

    #The following method will download the entire archive
    publico.download_all()

    #The following method use will download all the dates from 5th May 2024 to the 8th October 2005
    publico.download_d1_d2(d1=datetime.datetime(day=5,month=5,year=2024),d2=datetime.datetime(day=8,month=10,year=2024))

    #The following method use will download the latest front pages
    publico.download_latest()
