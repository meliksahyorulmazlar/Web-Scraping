#Duma webscraper.Duma is a newspaper in Bulgaria (Duma in Bulgarian means word)


import requests,os,lxml,datetime
from bs4 import BeautifulSoup


class Duma:
    def __init__(self):
        #initial start date of the archive: 5th January 2009
        self.initial_date = datetime.datetime(day=5,month=1,year=2009)
        self.one_day = datetime.timedelta(days=1)
        self.get_today()


    #finds the date of today
    #Do not use the method,the method is used for initialisation of the class
    def get_today(self):
        d = datetime.datetime.now().day
        m = datetime.datetime.now().month
        y = datetime.datetime.now().year
        self.final_date  = datetime.datetime(day=d,month=m,year=y)

    #This will download all of the Duma newspapers from the 5th February 2009 till today
    def download_all(self):
        start = self.initial_date
        end = self.final_date
        while start <= end:
            self.download_date(start)
            start += self.one_day

    #This will download any year between 2009 and the year that we are currently in
    def download_year(self,year:int):
        if year >= 2009:
            initial_date = datetime.datetime(day=1,month=1,year=year)
            final_date = datetime.datetime(day=31,month=12,year=year)
            while initial_date <= final_date:
                self.download_date(initial_date)
                initial_date += self.one_day

    #tuple(day,month,year)
    #lets say you want to download from 9th March 2018 til 15th september 2019
    #download(date1=(9,3,2018),date2=(15,9,2019)) is an example usage of the following method
    def download_d1_d2(self,date1:datetime.datetime,date2:datetime.datetime):
        if date1 > date2:
            c = date1
            date1 = date2
            date2 = c

        initial_date = date1
        final_date = date2
        year = date1[2]
        if year >= 2009:
            if initial_date < final_date:
                while initial_date <= final_date:
                    self.download_date(initial_date)
                    initial_date += self.one_day

    #This will download the newspaper for today
    def download_today(self):
        self.download_date(date=self.final_date)

    #The following method will download a specific date
    def download_date(self,date:datetime.datetime):
        day = date.day
        month = date.month
        year = date.year
        website = f"https://duma.bg/?go=newspaper&p=list&year={year}&month={month}&day={day}"

        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        try:
            pdf_link = soup.find("a", href=True, class_="dwnl_newspaper_item")["href"]
        except TypeError:
            pass
        else:
            pdf_link = "https://duma.bg/" + pdf_link
            filename = f"{day}-{month}-{year}.pdf"

            response = requests.get(url=pdf_link)
            if response.status_code == 200:
                with open(f"{filename}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", 'a') as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt", 'a') as f:
                    f.write(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                print(f"{filename}  was not downloaded, it had status code {response.status_code}\n")

    # This method will check if the pdf for a particular date has been downloaded or nor
    def check_date(self,date:datetime.datetime):
        day = date.day
        month = date.month
        year = date.year
        website = f"https://duma.bg/?go=newspaper&p=list&year={year}&month={month}&day={day}"

        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        try:
            pdf_link = soup.find("a", href=True, class_="dwnl_newspaper_item")["href"]
        except TypeError:
            pass
        else:
            pdf_link = "https://duma.bg/" + pdf_link
            filename = f"{day}-{month}-{year}.pdf"
            if filename not in os.listdir():
                response = requests.get(url=pdf_link)
                if response.status_code == 200:
                    with open(f"{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt", 'a') as f:
                        f.write(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                    print(f"{filename}  was not downloaded, it had status code {response.status_code}\n")

    #The following method will check from one date to another
    def check_d1_d2(self,date1:datetime.datetime,date2:datetime.datetime):
        if date1 > date2:
            c = date1
            date1 = date2
            date2 = c

        initial_date = date1
        final_date = date2
        year = date1[2]
        if year >= 2009:
            if initial_date < final_date:
                while initial_date <= final_date:
                    self.check_date(initial_date)
                    initial_date += self.one_day

    #The following method will check all the dates to see if they have been downloaded or not
    def check_all(self):
        date1 = self.initial_date
        date2 = self.final_date
        self.check_d1_d2(date1,date2)


if __name__ == "__main__":
    d = Duma()

    #The following method will download today's paper
    #Takes no input
    #d.download_today()

    #The following method will download all the newspapers for that year(any year from 2009 to the current year)
    #The input should be an integer
    #d.download_year(year=2010)

    #This will download all the newspapers from January 5 2009 till today
    #takes no input
    #d.download_all()

    #The following method will download all the newspapers from date1 to date2
    #date2 should be after date1
    #the inputs for date1 and date2 should be as a tuple
    #if date1 is 1st october 2018 and date2 is 30th June 2021
    #date1 should be (1,10,2018) and date2 should be (30,6,2021)
    #d.download(date1=(1,10,2018),date2=(30,6,2021))


