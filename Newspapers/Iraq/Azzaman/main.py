# Azzaman, Iraqi Newspaper
import os

import requests,lxml
from bs4 import BeautifulSoup
from tensorflow.python.ops.summary_ops_v2 import write


class Azzaman:
    # There are
    def __init__(self):
        self.international = 'https://www.azzaman.com/archives/?dir=pdf/pdfarchive'
        self.iraq = 'https://www.azzaman.com/archives/?dir=pdf/qpdfarchive'
        self.sports = 'https://www.azzaman.com/archives/?dir=pdf/spdfarchive'
        self.international_years = []
        self.iraq_years = []
        self.sports_years = []
        self.gather_years()
        self.start_folders()

    # The following method will print all the valid years for the sports edition
    def print_sports_years(self):
        print(self.sports_years)

    # The following method will print all the valid years for the Iraq edition
    def print_iraq_years(self):
        print(self.iraq_years)

    # The following method will print all the valid years for the International edition
    def print_international_years(self):
        print(self.international_years)

    # The following method start all the folders
    def start_folders(self):
        try:
            os.mkdir("Sports")
        except FileExistsError:
            pass
        try:
            os.mkdir("International")
        except FileExistsError:
            pass
        try:
            os.mkdir("Iraq")
        except FileExistsError:
            pass


    # The following method will gather all the years for each category
    def gather_years(self):
        soup = BeautifulSoup(requests.get(self.international).text,'lxml')
        years = [year['href'] for year in soup.find_all('a',href=True,class_='clearfix') if '/' in year['href']][1:]
        self.international_years = [int(year.split("/")[-1]) for year in years]

        soup = BeautifulSoup(requests.get(self.iraq).text,'lxml')
        years = [year['href'] for year in soup.find_all('a',href=True,class_='clearfix') if '/' in year['href']][1:]
        self.iraq_years = [int(year.split("/")[-1]) for year in years]

        soup = BeautifulSoup(requests.get(self.sports).text, 'lxml')
        years = [year['href'] for year in soup.find_all('a', href=True, class_='clearfix') if '/' in year['href']][1:]
        self.sports_years = [int(year.split("/")[-1]) for year in years]

    # The following method will download a specific year for the international edition
    def download_international_year(self,year:int):
        if year in self.international_years:
            os.mkdir(f"International/{year}")
            website = f"{self.international}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text,'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                os.mkdir(f"International/{year}/{month}")
                website = f"{self.international}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    os.mkdir(f"International/{year}/{month}/{day}")
                    website = f"{self.international}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if '/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        code = self.international.split("/")[-1]
                        print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                        response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                        if response.status_code == 200:
                            with open(f"International/{year}/{month}/{day}/{pdf}",'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt','a') as f:
                                f.write(f"International/{year}/{month}/{day}/{pdf} was downloaded.\n")
                            print(f"International/{year}/{month}/{day}/{pdf} was downloaded.")
                        else:
                            with open('download_results.txt','a') as f:
                                f.write(f"International/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                            print(f"International/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")

    # The following method will check a specific year for the international edition
    def check_international_year(self,year:int):
        if year in self.international_years:
            try:
                os.mkdir(f"International/{year}")
            except FileExistsError:
                pass
            website = f"{self.international}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text, 'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                try:
                    os.mkdir(f"International/{year}/{month}")
                except FileExistsError:
                    pass
                website = f"{self.international}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    try:
                        os.mkdir(f"International/{year}/{month}/{day}")
                    except FileExistsError:
                        pass
                    website = f"{self.international}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if'/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        if pdf not in os.listdir(f'International/{year}/{month}/{day}'):
                            code = self.international.split("/")[-1]
                            print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            if response.status_code == 200:
                                with open(f"International/{year}/{month}/{day}/{pdf}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"International/{year}/{month}/{day}/{pdf} was downloaded.\n")
                                print(f"International/{year}/{month}/{day}/{pdf} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"International/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                                print(f"International/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")
                        else:
                            print(f"{pdf} was already downloaded.")

    # The following method will download a specific year for the sports edition
    def download_sports_year(self,year:int):
        if year in self.sports_years:
            os.mkdir(f"Sports/{year}")
            website = f"{self.sports}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text, 'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                os.mkdir(f"Sports/{year}/{month}")
                website = f"{self.international}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    os.mkdir(f"Sports/{year}/{month}/{day}")
                    website = f"{self.sports}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if '/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        code = self.sports.split("/")[-1]
                        print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                        response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                        if response.status_code == 200:
                            with open(f"Sports/{year}/{month}/{day}/{pdf}", 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"Sports/{year}/{month}/{day}/{pdf} was downloaded.\n")
                            print(f"Sports/{year}/{month}/{day}/{pdf} was downloaded.")
                        else:
                            with open('download_results.txt', 'a') as f:
                                f.write(f"Sports/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                            print(f"Sports/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")

    # The following method will check a specific year for the sports Edition
    def check_sports_year(self,year:int):
        if year in self.sports_years:
            try:
                os.mkdir(f"Sports/{year}")
            except FileExistsError:
                pass
            website = f"{self.sports}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text, 'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                try:
                    os.mkdir(f"Sports/{year}/{month}")
                except FileExistsError:
                    pass
                website = f"{self.international}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    try:
                        os.mkdir(f"Sports/{year}/{month}/{day}")
                    except FileExistsError:
                        pass
                    website = f"{self.sports}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if '/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        if pdf not in os.listdir(f"Sports/{year}/{month}/{day}"):
                            code = self.sports.split("/")[-1]
                            print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            if response.status_code == 200:
                                with open(f"Sports/{year}/{month}/{day}/{pdf}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Sports/{year}/{month}/{day}/{pdf} was downloaded.\n")
                                print(f"Sports/{year}/{month}/{day}/{pdf} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Sports/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                                print(f"Sports/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")
                        else:
                            print(f"{pdf} was already downloaded")

    # The following method will download a specific year for the Iraqi edition
    def download_iraq_year(self,year:int):
        if year in self.iraq_years:
            try:
                os.mkdir(f"Iraq/{year}")
            except FileExistsError:
                pass
            website = f"{self.iraq}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text, 'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                try:
                    os.mkdir(f"Iraq/{year}/{month}")
                except FileExistsError:
                    pass
                website = f"{self.iraq}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    try:
                        os.mkdir(f"Iraq/{year}/{month}/{day}")
                    except FileExistsError:
                        pass
                    website = f"{self.iraq}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if '/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        if pdf not in os.listdir(f"Iraq/{year}/{month}/{day}"):
                            code = self.iraq.split("/")[-1]
                            print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            if response.status_code == 200:
                                with open(f"Iraq/{year}/{month}/{day}/{pdf}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Iraq/{year}/{month}/{day}/{pdf} was downloaded.\n")
                                print(f"Iraq/{year}/{month}/{day}/{pdf} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Iraq/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                                print(f"Iraq/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")
                        else:
                            print(f"{pdf} was already downloaded.")

    # The following method will check a specific year for the Iraqi edition
    def check_iraq_year(self,year:int):
        if year in self.iraq_years:
            try:
                os.mkdir(f"Iraq/{year}")
            except FileExistsError:
                pass
            website = f"{self.iraq}/{year}"
            month_soup = BeautifulSoup(requests.get(website).text, 'lxml')
            months = [month['href'] for month in month_soup.find_all('a', href=True, class_='clearfix') if '/' in month['href']][1:]
            months = [month.split("/")[-1] for month in months]
            for month in months:
                try:
                    os.mkdir(f"Iraq/{year}/{month}")
                except FileExistsError:
                    pass
                website = f"{self.iraq}/{year}/{month}"
                day_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                days = [day['href'] for day in day_soup.find_all('a', href=True, class_='clearfix') if '/' in day['href']][1:]
                days = [day.split("/")[-1] for day in days]
                for day in days:
                    try:
                        os.mkdir(f"Iraq/{year}/{month}/{day}")
                    except FileExistsError:
                        pass
                    website = f"{self.iraq}/{year}/{month}/{day}"
                    pdf_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                    pdfs = [pdf['href'] for pdf in pdf_soup.find_all('a', href=True, class_='clearfix') if '/' in pdf['href']][1:]
                    pdfs = [pdf.split("/")[-1] for pdf in pdfs]
                    for pdf in pdfs:
                        if pdf not in os.listdir(f"Iraq/{year}/{month}/{day}"):
                            code = self.iraq.split("/")[-1]
                            print(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            response = requests.get(f"https://www.azzaman.com/archives/pdf/{code}/{year}/{month}/{day}/{pdf}")
                            if response.status_code == 200:
                                with open(f"Iraq/{year}/{month}/{day}/{pdf}", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Iraq/{year}/{month}/{day}/{pdf} was downloaded.\n")
                                print(f"Iraq/{year}/{month}/{day}/{pdf} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"Iraq/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.\n")
                                print( f"Iraq/{year}/{month}/{day}/{pdf} was not downloaded, it had response status code {response.status_code}.")
                        else:
                            print(f"{pdf} was already downloaded")

    # The following method will download all the years from one year to another later year for the international edition
    def download_international_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c
            for year in range(y1,y2+1):
                self.download_international_year(year)

    # The following method will download all the years from one year to another later year for the sports edition
    def download_sports_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c

            for year in range(y1,y2+1):
                self.download_sports_year(year)

    # The following method will download all the years from one year to another later year for the Iraqi edition
    def download_iraqi_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c
            for year in range(y1,y2+1):
                self.download_iraq_year(year)

    # The following method will download the entire sports archive
    def download_all_sports(self):
        for year in self.sports_years:
            self.download_sports_year(year)

    # The following method will download the entire sports archive
    def download_all_iraq(self):
        for year in self.iraq_years:
            self.download_iraq_year(year)

    # The following method will download the entire international archive
    def download_all_international(self):
        for year in self.international_years:
            self.download_international_year(year)

    # The following method will download all the years from one year to another later year for the international edition
    def check_international_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c
            for year in range(y1,y2+1):
                self.check_international_year(year)

    # The following method will download all the years from one year to another later year for the sports edition
    def check_sports_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c

            for year in range(y1,y2+1):
                self.check_sports_year(year)

    # The following method will download all the years from one year to another later year for the Iraqi edition
    def check_iraqi_y1_y2(self,y1:int,y2:int):
        if y1 > y2:
            c = y1
            y1 = y2
            y2 = c
            for year in range(y1,y2+1):
                self.check_iraq_year(year)

    # The following method will check the entire sports archive
    def check_all_sports(self):
        for year in self.sports_years:
            self.check_sports_year(year)

    # The following method will check the entire sports archive
    def check_all_iraq(self):
        for year in self.iraq_years:
            self.check_iraq_year(year)

    # The following method will check the entire international archive
    def check_all_international(self):
        for year in self.international_years:
            self.check_international_year(year)

    # The following method will download all the categories
    def download_categories(self):
        self.download_all_sports()
        self.download_all_iraq()
        self.download_all_international()

    # The following method will check all the categories
    def check_categories(self):
        self.check_all_sports()
        self.check_all_iraq()
        self.check_all_international()

if __name__ == "__main__":
    azzaman = Azzaman()
    azzaman.check_all_sports()