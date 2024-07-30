# The New York Post Front and back page webscraper
# The New York Post is a famous daily tabloid published in New York City


import requests,os,lxml,datetime
from bs4 import BeautifulSoup


class NewYorkPost:
    def __init__(self):
        self.start_date = datetime.datetime(day=1, month=1, year=2002)
        self.today = self.return_today()
        self.month_dictionary = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        self.one_day = datetime.timedelta(days=1)

    # This method will return today's date
    def return_today(self) -> datetime.datetime:
        today = datetime.datetime.today()
        day = today.day
        month = today.month
        year = today.year
        return datetime.datetime(day=day, month=month, year=year)


    # This method will download any date between the 1st January 2002 and today
    def download_date(self, date: datetime.datetime):
        if self.start_date <= date <= self.today:
            self.different_links = {datetime.datetime(2013, 11, 12, 0, 0): 'https://nypost.com/cover/1688225/', datetime.datetime(2014, 1, 2, 0, 0): 'https://nypost.com/cover/covers-for-jan-2-2014/', datetime.datetime(2014, 1, 11, 0, 0): 'https://nypost.com/cover/covers-on-jan-14-2014/', datetime.datetime(2014, 1, 13, 0, 0): 'https://nypost.com/cover/covers-for-jan-13-2014/', datetime.datetime(2014, 1, 14, 0, 0): 'https://nypost.com/cover/covers-for-jan-13-2013/', datetime.datetime(2014, 1, 27, 0, 0): 'https://nypost.com/cover/covers-for-jan-27-2014/', datetime.datetime(2014, 1, 28, 0, 0): 'https://nypost.com/cover/covers-for-jan-27-2014-2/', datetime.datetime(2014, 2, 18, 0, 0): 'https://nypost.com/cover/3006908/', datetime.datetime(2014, 6, 16, 0, 0): 'https://nypost.com/cover/5866082/', datetime.datetime(2015, 2, 2, 0, 0): 'https://nypost.com/cover/covers-for-february-2-2015/', datetime.datetime(2015, 2, 16, 0, 0): 'https://nypost.com/cover/covers-for-february-16-2015/', datetime.datetime(2015, 2, 17, 0, 0): 'https://nypost.com/cover/covers-for-february-16-2015-2/', datetime.datetime(2015, 3, 2, 0, 0): 'https://nypost.com/cover/covers-for-march-2-2015/', datetime.datetime(2015, 3, 3, 0, 0): 'https://nypost.com/cover/covers-for-march-2-2015-2/', datetime.datetime(2015, 3, 8, 0, 0): 'https://nypost.com/cover/9580636/', datetime.datetime(2015, 3, 15, 0, 0): 'https://nypost.com/cover/9591888/', datetime.datetime(2015, 4, 2, 0, 0): 'https://nypost.com/cover/covers-for-april-2-2015/', datetime.datetime(2015, 6, 2, 0, 0): 'https://nypost.com/cover/covers-for-june-02-2015/', datetime.datetime(2015, 6, 7, 0, 0): 'https://nypost.com/cover/covers-for-june-7-2015/', datetime.datetime(2015, 4, 15, 0, 0): 'https://nypost.com/cover/9638748/', datetime.datetime(2015, 6, 8, 0, 0): 'https://nypost.com/cover/covers-for-june-7-2015-2/', datetime.datetime(2016, 3, 2, 0, 0): 'https://nypost.com/cover/covers-for-march-2-2016/', datetime.datetime(2016, 3, 7, 0, 0): 'https://nypost.com/cover/covers-for-march-7-2016/', datetime.datetime(2016, 3, 8, 0, 0): 'https://nypost.com/cover/covers-for-march-7-2016-2/', datetime.datetime(2016, 6, 8, 0, 0): 'https://nypost.com/cover/10229325/', datetime.datetime(2016, 9, 21, 0, 0): 'https://nypost.com/cover/10412836/', datetime.datetime(2016, 10, 6, 0, 0): 'https://nypost.com/cover/10445900/', datetime.datetime(2016, 10, 14, 0, 0): 'https://nypost.com/cover/10463550/', datetime.datetime(2016, 10, 20, 0, 0): 'https://nypost.com/cover/10477457/', datetime.datetime(2016, 11, 2, 0, 0): 'https://nypost.com/cover/10508076/', datetime.datetime(2016, 11, 6, 0, 0): 'https://nypost.com/cover/covers-for-november-7-2016/', datetime.datetime(2016, 11, 7, 0, 0): 'https://nypost.com/cover/covers-for-november-7-2016-2/', datetime.datetime(2016, 11, 10, 0, 0): 'https://nypost.com/cover/10527446/', datetime.datetime(2016, 11, 16, 0, 0): 'https://nypost.com/cover/10542179/', datetime.datetime(2016, 11, 24, 0, 0): 'https://nypost.com/cover/covers-for-november-24-2016/', datetime.datetime(2016, 11, 25, 0, 0): 'https://nypost.com/cover/covers-for-november-24-2016-2/', datetime.datetime(2017, 1, 1, 0, 0): 'https://nypost.com/cover/covers-for-january-1-2017/', datetime.datetime(2017, 1, 7, 0, 0): 'https://nypost.com/cover/covers-for-january-1-2017-2/', datetime.datetime(2017, 3, 2, 0, 0): 'https://nypost.com/cover/10774241/', datetime.datetime(2017, 3, 23, 0, 0): 'https://nypost.com/cover/10821553/', datetime.datetime(2017, 6, 2, 0, 0): 'https://nypost.com/cover/covers-for-june-2-2017/', datetime.datetime(2017, 6, 7, 0, 0): 'https://nypost.com/cover/covers-for-june-7-2017/', datetime.datetime(2017, 6, 8, 0, 0): 'https://nypost.com/cover/covers-for-june-7-2017-2/', datetime.datetime(2018, 2, 16, 0, 0): 'https://nypost.com/cover/covers-february-162018/', datetime.datetime(2018, 12, 1, 0, 0): 'https://nypost.com/cover/covers-12-01-2018/', datetime.datetime(2018, 12, 4, 0, 0): 'https://nypost.com/cover/covers-for-tuesday-december-4-2018/', datetime.datetime(2018, 12, 12, 0, 0): 'https://nypost.com/cover/covers-for-wednesday-december-12-2018/', datetime.datetime(2018, 12, 15, 0, 0): 'https://nypost.com/cover/covers-for-saturday-december-15-2018/', datetime.datetime(2018, 12, 17, 0, 0): 'https://nypost.com/cover/covers-for-tuesday-december-4-2018/', datetime.datetime(2019, 3, 1, 0, 0): 'https://nypost.com/cover/march-1-2019/', datetime.datetime(2019, 5, 15, 0, 0): 'https://nypost.com/cover/covers-for-wednesday-may-15-2019/', datetime.datetime(2019, 5, 16, 0, 0): 'https://nypost.com/cover/5-15-2019/', datetime.datetime(2019, 10, 15, 0, 0): 'https://nypost.com/cover/covers-for-tuesday-october-16-2019/', datetime.datetime(2019, 12, 28, 0, 0): 'https://nypost.com/cover/saturday-december-29-2019/', datetime.datetime(2020, 1, 14, 0, 0): 'https://nypost.com/cover/covers-for-tuesday-january-14-2020/', datetime.datetime(2020, 1, 15, 0, 0): 'https://nypost.com/cover/covers-for-wednesday-january-14-2020/', datetime.datetime(2020, 2, 4, 0, 0): 'https://nypost.com/cover/covers-for-tuesday-january-4-2020/', datetime.datetime(2020, 2, 5, 0, 0): 'https://nypost.com/cover/covers-for-wednesday-february-4-2020/', datetime.datetime(2020, 4, 11, 0, 0): 'https://nypost.com/cover/covers-for-saturday-april-11-2020/', datetime.datetime(2020, 4, 12, 0, 0): 'https://nypost.com/cover/covers-for-saturday-april-11-2020-2/', datetime.datetime(2020, 7, 13, 0, 0): 'https://nypost.com/cover/july-13-2020/', datetime.datetime(2020, 7, 14, 0, 0): 'https://nypost.com/cover/july-13-2020-2/', datetime.datetime(2020, 8, 5, 0, 0): 'https://nypost.com/cover/august-52020/', datetime.datetime(2020, 10, 1, 0, 0): 'https://nypost.com/cover/september-31-2020/', datetime.datetime(2020, 11, 6, 0, 0): 'https://nypost.com/cover/november-6-2020/', datetime.datetime(2020, 11, 7, 0, 0): 'https://nypost.com/cover/november-6-2020-2/', datetime.datetime(2021, 2, 28, 0, 0): 'https://nypost.com/cover/february-282021/', datetime.datetime(2021, 7, 2, 0, 0): 'https://nypost.com/cover/july-22;012/', datetime.datetime(2022, 6, 8, 0, 0): 'https://nypost.com/cover/june-9-2022/', datetime.datetime(2024, 5, 8, 0, 0): 'https://nypost.com/cover/may-8-2024/', datetime.datetime(2024, 5, 10, 0, 0): 'https://nypost.com/cover/may-8-2024-2/'}
            if date in self.different_links:
                formatted_date = f"{date.month}-{date.day}-{date.year}"
                self.download_link(formatted_date=formatted_date, website=self.different_links[date])
            else:
                self.download(date)

    #This method will find the link to download off of
    def download(self, date: datetime.datetime):
        month = date.month
        year = date.year
        day = date.day

        formatted_date = f"{month}-{day}-{year}"
        not_found = True

        if month < 10:
            ny_month = f"0{month}"
        else:
            ny_month = month

        # This will find the covers for that date's month
        website = f"https://nypost.com/{year}/{ny_month}/?post_type=cover"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        links = [link["href"] for link in soup.find_all("a", href=True) if
                 "cover" in link["href"] and "hamburger" not in link["href"] and link["href"] != "/covers/"]
        # conditions for suffices of words
        if day == 1 or day == 21 or day == 31:
            suffix = "st"
        elif day == 2 or day == 22:
            suffix = "nd"
        elif day == 3 or day == 23:
            suffix = "rd"
        else:
            suffix = "th"

        # Possible conditions to find a date
        total_suffix = f"{day}{suffix}"  # 1st
        string_day = str(day)  # "1"
        zero_day = f"0{day}"  # "01"
        print(links)
        for link in links:
            splits = [split.strip("/") for split in link.split("-")]
            for split in splits:
                if (split == total_suffix or split == string_day or split == zero_day) and not_found:
                    not_found = False
                    self.download_link(formatted_date=formatted_date, website=link)

        if not_found:
            with open("download_results.txt", "a") as f:
                f.write(f"{formatted_date} was not found\n")
            print(f"{formatted_date} was not found")

    #This method will download the link
    def download_link(self,formatted_date:str,website:str):
        os.makedirs(formatted_date, exist_ok=True)
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        images = [image["src"].split("?")[0] for image in soup.find_all("img", src=True) if "nypost" in image["src"]]

        for image in images:
            filename = image.split("/")[-1]
            response = requests.get(url=image)

            if response.status_code == 200:
                with open(f"{formatted_date}/{filename}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{formatted_date}/{filename} was downloaded\n")
                print(f"{formatted_date}/{filename} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(
                        f"{formatted_date}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                print(
                    f"{formatted_date}/{filename} was not downloaded, it had response status code {response.status_code}")

    # This method will download all the covers from one date to another
    #download_d1(d1=datetime.datetime(day=1,month=1,year=2005),d2=datetime.datetime(day=5,month=1,year=2005))
    #The following method call will download:
    #The 1st,2nd,3rd,4th,5th January of 2005
    def download_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d2
            d2 = d1
            d1 = c
        print(d1)
        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # This method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date, d2=self.today)

    # The following method will download today's front and back page of the New York Post
    def download_today(self):
        self.download_date(date=self.today)

    # The following method will download yesterday's front and back page of the New York Post
    def download_yesterday(self):
        yesterday = self.today - self.one_day
        self.download_date(date=yesterday)

if __name__ == "__main__":
    nyp = NewYorkPost()
    nyp.download_all()
    #nyp.download_today()
    #nyp.download_yesterday()
    #nyp.download_d1_d2(d1=datetime.datetime(day=1,month=1,year=2024),d2=datetime.datetime(day=5,month=1,year=2024))
    #nyp.download_d1_d2(d1=datetime.datetime(day=1,month=5,year=2019),d2=datetime.datetime(day=31,month=5,year=2019))
    #nyp.redirect_download(date=datetime.datetime(day=11,month=1,year=2014))
    #nyp.download_d1_d2(d1=datetime.datetime(day=3,month=7,year=2024),d2=nyp.today)

