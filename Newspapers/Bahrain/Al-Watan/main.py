# Al-Watan, Bahrain Newspaper


import requests,lxml,datetime,os
from bs4 import BeautifulSoup


class AlWatanBahrain:
    def __init__(self):
        self.start_time = datetime.datetime(day=10,month=12,year=2005)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    # The following method will return today's date
    def return_today(self):
        t = datetime.datetime.now()
        day = t.day
        month = t.month
        year = t.year
        return datetime.datetime(day=day,month=month,year=year)

    # The following method will download a particular date:
    def download_date(self,date:datetime.datetime):
        day = date.day
        if day < 10:
            day = f"0{day}"
        month = date.month
        if month < 10:
            month = f"0{month}"
        year = date.year
        filename = f"watan-{year}{month}{day}.pdf"
        website = f"https://alwatannews.net/archive?datefrom={year}-{month}-{day}&dateto={year}-{month}-{day}"
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if ".pdf" in pdf['href']]
        if len(pdfs) == 2:
            print(f"There are no pdfs for this date: {day}-{month}-{year}")
        else:
            website = pdfs[-1]
            response = requests.get(website)
            if response.status_code == 200:
                with open(f"{filename}",'wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was downloaded.\n")
                print(f"{filename} was downloaded.")
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one date to another later date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_time,d2=self.today)

    # The following method will download a particular date:
    def check_date(self, date: datetime.datetime):
        day = date.day
        if day < 10:
            day = f"0{day}"
        month = date.month
        if month < 10:
            month = f"0{month}"
        year = date.year
        filename = f"watan-{year}{month}{day}.pdf"
        if filename not in os.listdir():
            website = f"https://alwatannews.net/archive?datefrom={year}-{month}-{day}&dateto={year}-{month}-{day}"
            soup = BeautifulSoup(requests.get(website).text, 'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if ".pdf" in pdf['href']]
            if len(pdfs) == 2:
                print(f"There are no pdfs for this date: {day}-{month}-{year}")
            else:
                website = pdfs[-1]
                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"{filename}", 'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")
        else:
            print(f"{filename} was already downloaded")

    # The following method will download from one date to another later date
    def check_d1_d2(self, d1: datetime.datetime, d2: datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def check_all(self):
        self.download_d1_d2(d1=self.start_time, d2=self.today)


if __name__ == "__main__":
    alb = AlWatanBahrain()
    alb.check_d1_d2(d1=alb.start_time,d2=alb.today)















