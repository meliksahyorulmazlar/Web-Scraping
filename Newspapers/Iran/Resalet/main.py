# Tehran Times pdf webscraper
# The Tehran Times is an English-language daily newspaper published in Iran
# It was founded in 1979 as the self-styled "voice of the Islamic Revolution".


import requests,os,lxml,datetime
from bs4 import BeautifulSoup


class TehranTimes:
    def __init__(self):
        #The Tehran Times archive started on the 5th March 2016
        self.month_number_dictionary = self.month_dictionary = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        self.number_month_dictionary = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        self.start_date = datetime.datetime(day=7,month=3,year=2016)
        self.latest_date = self.find_latest()
        self.one_day = datetime.timedelta(days=1)


    #This method will find the last day Tehran Times was published
    def find_latest(self)->datetime.datetime:
        website = "https://www.tehrantimes.com/archive?ty=14&ms=2&ps=30"
        soup = BeautifulSoup(requests.get(url=website).text,'lxml')

        span = soup.find("span",class_='item-time ltr',title=True)

        dates = span["title"].split()
        day = int(dates[1])
        month_string = dates[2]
        month = self.month_number_dictionary[month_string]
        year = int(dates[3])

        return datetime.datetime(day=day,month=month,year=year)

    # There are 2 dates where you can only download the front page
    # The dates were 13th March 2011 and 5th March 2015
    def download_cover(self,date:datetime.datetime):
        dictionary = {datetime.datetime(day=13,month=3,year=2011):"https://media.mehrnews.com/d/2016/02/23/4/2007585.jpg?ts=1486462047399",datetime.datetime(day=5,month=3,year=2016):"https://media.mehrnews.com/d/2016/03/05/4/2019086.jpg?ts=1486462047399"}
        if date in dictionary:
            image = dictionary[date]
            response = requests.get(url=image)

            formatted_date = f"{date.day}-{date.month}-{date.year}"
            no = 11211
            file_name = f"{no}-({formatted_date})"

            try:
                os.mkdir(f"{date.year}")
            except FileExistsError:
                pass

            try:
                os.mkdir(f"{date.year}/{date.month} {self.number_month_dictionary[date.month]}")
            except FileExistsError:
                pass

            if response.status_code == 200:
                with open(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}/{file_name}.jpg", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{file_name} was downloaded\n")
                print(f"{file_name} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{file_name} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{file_name} was downloaded,it had response status code {response.status_code}")

    # This method will check if there are any pdfs to download for a particular given date and download it
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.latest_date:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{date.day}-{date.month}-{date.year}"

            website = f"https://www.tehrantimes.com/archive?pi=1&ty=14&ms=2&ps=2&dy={day}&mn={month}&yr={year}"

            soup = BeautifulSoup(requests.get(url=website).text,"lxml")

            lis = soup.find_all("li",class_="mosaic mosaic-2 newspaper")
            count = 1
            for li in lis:
                word_date = f"{day} {self.number_month_dictionary[month]} {year}"
                span = li.find("span",title=True)
                title = span["title"]
                if word_date in title:
                    anchor_tag = li.find("a",href=True)
                    href = anchor_tag["href"]
                    no = href.split("/")[-1]
                    file_name = f"{no}-({formatted_date})"
                    download_link = f"https://www.tehrantimes.com{href}"

                    try:
                        os.mkdir(f"{date.year}")
                    except FileExistsError:
                        pass

                    try:
                        os.mkdir(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}")
                    except FileExistsError:
                        pass

                    response = requests.get(url=download_link)
                    if response.status_code == 200:
                        with open(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}/{file_name}-{count}.pdf", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{file_name}-{count} was downloaded\n")
                        print(f"{file_name}-{count} was downloaded")
                        count += 1
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(f"{file_name} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{file_name} not was downloaded,it had response status code {response.status_code}")

    # The following method will download all the pdfs from one date to another
    # example: download_d1_d2(d1=datetime.datetime(day=1,month=1,year=2017),d2=datetime.datetime(day=1,month=2,year=2017)_
    # The following example will download all the dates from the 1st January 2017 till the 1st February 2017
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = d1

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will download the entire pdf archive
    # from the 7th March 2016 till the latest day Tehran Times was published on the archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.latest_date)

    #This method will download the latest pdf of Tehran Times
    def download_latest_date(self):
        self.download_date(date=self.latest_date)

    # The following method will check if the pdf has been downloaded or not
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.latest_date:
            day = date.day
            month = date.month
            year = date.year
            formatted_date = f"{date.day}-{date.month}-{date.year}"

            website = f"https://www.tehrantimes.com/archive?pi=1&ty=14&ms=2&ps=2&dy={day}&mn={month}&yr={year}"

            soup = BeautifulSoup(requests.get(url=website).text, "lxml")

            lis = soup.find_all("li", class_="mosaic mosaic-2 newspaper")
            count = 1
            for li in lis:
                word_date = f"{day} {self.number_month_dictionary[month]} {year}"
                span = li.find("span", title=True)
                title = span["title"]
                if word_date in title:
                    anchor_tag = li.find("a", href=True)
                    href = anchor_tag["href"]
                    no = href.split("/")[-1]
                    file_name = f"{no}-({formatted_date})"
                    download_link = f"https://www.tehrantimes.com{href}"

                    try:
                        os.mkdir(f"{date.year}")
                    except FileExistsError:
                        pass

                    try:
                        os.mkdir(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}")
                    except FileExistsError:
                        pass

                    if f"{file_name}-{count}.pdf" not in os.listdir(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}"):
                        response = requests.get(url=download_link)
                        if response.status_code == 200:
                            with open(f"{date.year}/{date.month}{self.number_month_dictionary[date.month]}/{file_name}-{count}.pdf","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{file_name}-{count} was downloaded\n")
                            print(f"{file_name}-{count} was downloaded")
                            count += 1
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(
                                    f"{file_name} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{file_name} not was downloaded,it had response status code {response.status_code}")

    # The following method will check from one date to another
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetimea):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = d1

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        start = self.start_date
        end = self.latest_date
        self.check_d1_d2(start,end)

if __name__ == "__main__":
    tt = TehranTimes()
    tt.download_all()
