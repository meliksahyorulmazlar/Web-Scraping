# Al Raya- Qatari Newspaper

import datetime,requests,os,time
from urllib.parse import unquote
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

class AlRaya:
    def __init__(self):
        self.start_driver()
        self.early_date = datetime.datetime(day=14,month=4,year=2006)
        self.minimum_date = datetime.datetime(day=15,month=1,year=2007)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    def start_driver(self):
        options = uc.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=options)
        self.driver.get('https://www.raya.com/%D8%A7%D8%B1%D8%B4%D9%8A%D9%81-%D8%A7%D9%84%D8%B1%D8%A7%D9%8A%D8%A9/?date_from=2007-01-19&date_to=2007-01-19')
        time.sleep(6)

    # The following method will return today's date
    def return_today(self):
        t = datetime.datetime.now()
        day = t.day
        month = t.month
        year = t.year
        return datetime.datetime(day=day,month=month,year=year)

    # The following method will download a specific date
    def download_date(self,date:datetime.datetime):
        if date == self.early_date or self.minimum_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            directory_name = f"{day}-{month}-{year}"
            os.mkdir(f"{directory_name}")
            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"
            site = f"https://www.raya.com/ارشيف-الراية/?date_from={year}-{month}-{day}&date_to={year}-{month}-{day}"
            print(site)
            self.driver.get(site)
            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            do_not = ['https://assets.raya.com/wp-content/uploads/2023/01/30085058/Mediakit_2023_REVISED.pdf', 'https://assets.raya.com/wp-content/uploads/2023/01/30085109/Raya_media_kit-.pdf']
            pdfs = list(set([pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href'] and pdf['href'] not in do_not]))
            print(pdfs)
            for pdf in pdfs:
                filename = unquote(pdf.split("/")[-1])
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"{directory_name}/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{directory_name}/{filename} was downloaded.\n")
                    print(f"{directory_name}/{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{directory_name}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{directory_name}/{filename} was not downloaded, it had response status code {response.status_code}")

            if len(os.listdir(f"{directory_name}")) == 0:
                os.rmdir(directory_name)
                print(f"{directory_name} had no pdfs")
    # The following method will check one date
    def check_date(self,date:datetime.datetime):
        if date == self.early_date or self.minimum_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year
            directory_name = f"{day}-{month}-{year}"
            try:
                os.mkdir(f"{directory_name}")
            except FileExistsError:
                pass
            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"
            site = f"https://www.raya.com/ارشيف-الراية/?date_from={year}-{month}-{day}&date_to={year}-{month}-{day}"
            print(site)
            self.driver.get(site)
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            do_not = ['https://assets.raya.com/wp-content/uploads/2023/01/30085058/Mediakit_2023_REVISED.pdf', 'https://assets.raya.com/wp-content/uploads/2023/01/30085109/Raya_media_kit-.pdf']
            pdfs = list(set([pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href'] and pdf['href'] not in do_not]))
            print(pdfs)
            for pdf in pdfs:
                filename = unquote(pdf.split("/")[-1])
                if filename not in os.listdir(directory_name):
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{directory_name}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{directory_name}/{filename} was downloaded.\n")
                        print(f"{directory_name}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{directory_name}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{directory_name}/{filename} was not downloaded, it had response status code {response.status_code}")
            if len(os.listdir(f"{directory_name}")) == 0:
                os.rmdir(directory_name)
                print(f"{directory_name} had no pdfs")

    # The folllowing method will download from one date to another
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = d1

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The folllowing method will download from one date to another date
    def check_d1_d2(self, d1: datetime.datetime, d2: datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = d1

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will check all the dates
    def check_all(self):
        self.check_d1_d2(d1=self.early_date,d2=self.today)

    # The following method will check all the dates
    def download_all(self):
        self.download_d1_d2(d1=self.early_date,d2=self.today)

if __name__ == "__main__":
    raya = AlRaya()
    raya.download_all()