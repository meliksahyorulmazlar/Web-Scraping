# Teesdale Mercury Archive
import os

import requests,lxml,datetime
from bs4 import BeautifulSoup


class TeesdaleMercury:
    def __init__(self):
        self.first_day = datetime.datetime(day=4,month=7,year=1855)
        self.last_date = datetime.datetime(day=21,month=12,year=2005)
        self.one_day = datetime.timedelta(days=1)
        self.headers  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Referer": "http://online.osul.com.br/edicoesanteriores/"}
        self.dictionary = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}



    # The following method will check if there is a pdf for that particular date if there is one, it will download it
    def download_date(self,date:datetime.datetime):
        if self.first_day <= date <= self.last_date:
            day = date.day
            month = date.month
            year = date.year

            month_text = self.dictionary[month]
            if day < 10:
                day_code = f"0{day}"
            else:
                day_code = str(day)

            if month < 10:
                month_code = f"0{day}"
            else:
                month_code = str(month)
            number = 1

            number_code = f"0{number}"
            pdf_link = f"http://teesdalemercuryarchive.org/pdf/{year}/{month_text}-{day_code}/{month_text}-{day_code}-{year}-{number_code}.pdf"
            response = requests.get(url=pdf_link, headers=self.headers)
            if response.status_code == 200:
                filename = pdf_link.split("/")[-1]
                main_directory = filename.split("-01.pdf")[0]
                os.mkdir(main_directory)
                with open(f"{main_directory}/{filename}",'wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{main_directory}/{filename} was downloaded.\n")
                print(f"{main_directory}/{filename} was downloaded.")
                while True:
                    number += 1
                    if number < 10:
                        number_code = f"0{number}"
                    pdf_link = f"http://teesdalemercuryarchive.org/pdf/{year}/{month_text}-{day_code}/{month_text}-{day_code}-{year}-{number_code}.pdf"
                    response = requests.get(url=pdf_link, headers=self.headers)
                    if response.status_code == 200:
                        filename = pdf_link.split("/")[-1]
                        with open(f"{main_directory}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{main_directory}/{filename} was downloaded.\n")
                        print(f"{main_directory}/{filename} was downloaded.")
                    else:
                        break
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{day}-{month}-{year} was not downloaded/had no pdf, response status code: {response.status_code}\n")
                print(f"{day}-{month}-{year} was not downloaded/had no pdf, response status code: {response.status_code}")
                print(pdf_link)

    # The following method will download all the dates from one date to another later date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(self.first_day,self.last_date)

    #The following method will check if there is a pdf for that particular date if there is one, it will download it and if it has not been downloaded yet it will download the pdf
    def check_date(self,date:datetime.datetime):
        if self.first_day <= date <= self.last_date:
            day = date.day
            month = date.month
            year = date.year

            month_text = self.dictionary[month]
            if day < 10:
                day_code = f"0{day}"
            else:
                day_code = str(day)

            if month < 10:
                month_code = f"0{day}"
            else:
                month_code = str(month)
            number = 1

            number_code = f"0{number}"
            pdf_link = f"http://teesdalemercuryarchive.org/pdf/{year}/{month_text}-{day_code}/{month_text}-{day_code}-{year}-{number_code}.pdf"
            filename = pdf_link.split("/")[-1]
            main_directory = filename.split("-01.pdf")[0]
            try:
                os.listdir(main_directory)
            except FileNotFoundError:
                self.download_date(date)
            else:
                while True:
                    if number < 10:
                        number_code = f"0{number}"
                    pdf_link = f"http://teesdalemercuryarchive.org/pdf/{year}/{month_text}-{day_code}/{month_text}-{day_code}-{year}-{number_code}.pdf"
                    filename = pdf_link.split("/")[-1]
                    if filename not in os.listdir(main_directory):
                        response = requests.get(url=pdf_link, headers=self.headers)
                        if response.status_code == 200:

                            with open(f"{main_directory}/{filename}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{main_directory}/{filename} was downloaded.\n")
                            print(f"{main_directory}/{filename} was downloaded.")
                            number += 1
                        else:
                            break
                    else:
                        number += 1

    # The following method will check all the dates from one date to another later date
    def check_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.first_day, self.last_date)

if __name__ == "__main__":
    tm = TeesdaleMercury()
    tm.check_date(date=tm.first_day)
