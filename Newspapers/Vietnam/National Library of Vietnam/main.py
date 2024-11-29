# National Library of Vietnam Archives

import requests,lxml,os
from bs4 import BeautifulSoup

class NationalLibraryOfVietnam:
    def __init__(self):
        self.newspaper_dictionary = {}
        self.get_newspapers()

    # This method finds all the newspapers
    def get_newspapers(self):
        page = 'http://baochi.nlv.gov.vn/baochi/cgi-bin/baochi?a=cl&cl=CL1'
        soup = BeautifulSoup(requests.get(url=page).text,'lxml')
        for name in soup.select("li a",href=True):
            self.newspaper_dictionary[name.text] = f'http://baochi.nlv.gov.vn{name['href']}'



    # This method prints the names of all the newspapers
    def print_newspaper_names(self):
        for key in self.newspaper_dictionary:
            print(key)

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            os.mkdir(newspaper)
            page = self.newspaper_dictionary[newspaper]
            code = page.split("sp=")
            code = code[1].split("&")[0]
            print(page)
            month_soup = BeautifulSoup(requests.get(url=page).text,'lxml')
            months = [f"http://baochi.nlv.gov.vn{time['href']}" for time in month_soup.select('td a',href=True,class_='datebrowserrichardmonth') if 'cl=CL2.' in time['href']]
            for month in months:
                print(month)
                string = month.split("&")
                string.pop()
                string.pop()
                string = "&".join(string)
                list_form = string.split(".")

                month_format = ''
                year_format = ''
                for item in list_form:
                    if len(item) == 4:
                        year_format = item
                    elif len(item) == 2:
                        month_format = item

                os.mkdir(f"{newspaper}/{month_format}-{year_format}")


                days_soup = BeautifulSoup(requests.get(url=month).text,'lxml')
                days = [f"http://baochi.nlv.gov.vn{day['href']}" for day in days_soup.select('ul li a',href=True,class_='datebrowserrichardmonth') ]

                for day in days:

                    time = day.split(code)
                    time = time[1].split("&")[0]
                    print(time)
                    os.mkdir(f"{newspaper}/{month_format}-{year_format}/{time}")
                    loop = True
                    page_number = 1
                    while loop:
                        file  = f'http://baochi.nlv.gov.vn/baochi/cgi-bin/imageserver/imageserver.pl?color=all&ext=jpg&oid={code}{time}.1.{page_number}'
                        response = requests.get(url=file)
                        if response.status_code == 200:
                            with open(f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg','wb') as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg was downloaded.\n')
                            print(f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg was downloaded.')
                            page_number += 1
                        else:
                            break

    # The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)


    # The following method will check if all the images for that specific newspaper had been downloaded or not
    def check_newspaper(self,newspaper:str):
        try:
            files = os.listdir(newspaper)
        except FileNotFoundError:
            self.download_newspaper(newspaper)
        else:
            if newspaper in self.newspaper_dictionary:
                try:
                    os.mkdir(newspaper)
                except FileExistsError:
                    pass
                page = self.newspaper_dictionary[newspaper]
                code = page.split("sp=")
                code = code[1].split("&")[0]
                print(page)
                month_soup = BeautifulSoup(requests.get(url=page).text, 'lxml')
                months = [f"http://baochi.nlv.gov.vn{time['href']}" for time in month_soup.select('td a', href=True, class_='datebrowserrichardmonth') if 'cl=CL2.' in time['href']]
                for month in months:
                    print(month)
                    string = month.split("&")
                    string.pop()
                    string.pop()
                    string = "&".join(string)
                    list_form = string.split(".")

                    month_format = ''
                    year_format = ''
                    for item in list_form:
                        if len(item) == 4:
                            year_format = item
                        elif len(item) == 2:
                            month_format = item

                    try:
                        os.mkdir(f"{newspaper}/{month_format}-{year_format}")
                    except FileExistsError:
                        pass


                    days_soup = BeautifulSoup(requests.get(url=month).text, 'lxml')
                    days = [f"http://baochi.nlv.gov.vn{day['href']}" for day in days_soup.select('ul li a', href=True, class_='datebrowserrichardmonth')]

                    for day in days:

                        time = day.split(code)
                        time = time[1].split("&")[0]
                        print(time)
                        try:
                            os.mkdir(f"{newspaper}/{month_format}-{year_format}/{time}")
                        except FileExistsError:
                            pass
                        loop = True
                        page_number = 1
                        while loop:
                            file = f'http://baochi.nlv.gov.vn/baochi/cgi-bin/imageserver/imageserver.pl?color=all&ext=jpg&oid={code}{time}.1.{page_number}'
                            response = requests.get(url=file)
                            if f"{page_number}.jpg" not in os.listdir(f"{newspaper}/{month_format}-{year_format}/{time}"):
                                if response.status_code == 200:
                                    with open(f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg', 'wb') as f:
                                        f.write(response.content)
                                    with open("download_results.txt", "a") as f:
                                        f.write(
                                            f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg was downloaded.\n')
                                    print(f'{newspaper}/{month_format}-{year_format}/{time}/{page_number}.jpg was downloaded.')
                                    page_number += 1
                                else:
                                    break
                            else:
                                page_number += 1



    # The following method will check if all the images for all the newspapers had been downloaded or not
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)








if __name__ == "__main__":
    nlv = NationalLibraryOfVietnam()
    nlv.check_newspaper(newspaper='Vịt Đực')
