# L'Unità archive

import datetime,requests,os,lxml
from bs4 import BeautifulSoup

class Lunita:
    def __init__(self):
        self.first_date = datetime.datetime(day=2,month=1,year=1946)
        self.last_date = datetime.datetime(day=31,month=7,year=2014)
        self.one_day = datetime.timedelta(days=1)

    # The following method will download a specific date
    def download_date(self,date:datetime.datetime):
        if self.first_date <= date <=self.last_date:
            day = date.day
            month = date.month
            year = date.year

            date_string = f"{day}-{month}-{year}"
            if day < 10:
                day = f"0{day}"

            if month < 10:
                month = f"0{month}"


            site = f'https://archivio.unita.news/assets/derived/{year}/{month}/{day}/issue_full.pdf'
            response = requests.get(url=site)
            if response.status_code == 200:
                with open(f'{date_string}.pdf','wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{date_string}.pdf was downloaded.\n")
                print(f'{date_string}.pdf was downloaded.')
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{date_string}.pdf was not downloaded, it had response status code {response.status_code}.\n")
                print(f"{date_string}.pdf was not downloaded, it had response status code {response.status_code}.")




    # The following method will download the pdfs in a particular given range
    def download_range(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c
        print(d1,d2)
        while d1 <= d2:
            self.download_date(d1)
            print(d1)
            d1 += self.one_day

    # The following method will download all the pdfs from the 2nd January 1946 till the 31st July 2014
    def download_all(self):
        self.download_range(d1=self.first_date,d2=self.last_date)

    # This method if the pdf for that given date has been downloaded or not
    def check_date(self,date:datetime.datetime):
        day = date.day
        month = date.month
        year = date.year

        date_string = f"{day}-{month}-{year}"
        if f"{date_string}.pdf" not in os.listdir():
            if day < 10:
                day = f"0{day}"

            if month < 10:
                month = f"0{month}"

            site = f'https://archivio.unita.news/assets/derived/{year}/{month}/{day}/issue_full.pdf'
            response = requests.get(url=site)
            if response.status_code == 200:
                with open(f'{date_string}.pdf', 'wb') as f:
                    f.write(response.content)
                with open('download_results.txt', 'a') as f:
                    f.write(f"{date_string}.pdf was downloaded.\n")
                print(f'{date_string}.pdf was downloaded.')
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(f"{date_string}.pdf was not downloaded, it had response status code {response.status_code}.\n")
                print(f"{date_string}.pdf was not downloaded, it had response status code {response.status_code}.")


    # The following method will check the pdfs in a particular given range
    def check_range(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c
        print(d1,d2)
        while d1 <= d2:
            self.check_date(d1)
            print(d1)
            d1 += self.one_day

    # The following method will download all the pdfs from the 2nd January 1946 till the 31st July 2014
    def check_all(self):
        self.check_range(d1=self.first_date,d2=self.last_date)

if __name__ == "__main__":
    lunita = Lunita()
    lunita.download_all()