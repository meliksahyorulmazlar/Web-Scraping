# O Sul Newspaper

import datetime,lxml,requests,os
from bs4 import BeautifulSoup
from selenium import webdriver

class OSul:
    def __init__(self):
        self.first_month = (1,2006)
        self.last_month = self.return_current_month_year()
        self.months = self.get_all_months()
        self.start_webdriver()
        self.headers  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Referer": "http://online.osul.com.br/edicoesanteriores/"}

    # The following method will start the selenium webdriver
    def start_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)


    # The following method return the lastest month
    def return_current_month_year(self):
        t = datetime.datetime.now()
        month = t.month
        year = t.year
        return month,year

    # The following method will get all the months
    def get_all_months(self):
        months = [self.first_month]
        t1 = self.first_month
        t2 = self.last_month
        while t1 != t2:
            month = t1[0]
            if month < 12:
                new_t = month+1,t1[1]
                months.append(new_t)
                t1 = new_t
            else:
                new_t = 1,t1[1]+1
                months.append(new_t)
                t1 = new_t
        return months

    # The following method will print all the months on the archive
    def print_months(self):
        for month in self.months:
            print(month)

    def download_month(self,time:tuple):
        if time in self.months:
            month = time[0]
            year = time[1]
            if month < 10:
                month = f"0{month}"
            website = f'http://online.osul.com.br/edicoesanteriores/edicoes_anteriores_include.php?combo_data={month}/{year}'
            self.driver.get(website)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            times = [t['href'] for t in soup.find_all('a',href=True) if 'DATA' in t['href']]
            for t in times:
                print(t)
                response = requests.get(t,headers=self.headers)


                file_t = t.split("=")[-1]
                filename = f"OSul{file_t}.pdf"
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


    # The following method will check if a particular month has been downloaded or not
    def check_month(self,time:tuple):
        if time in self.months:
            month = time[0]
            year = time[1]
            if month < 10:
                month = f"0{month}"
            website = f'http://online.osul.com.br/edicoesanteriores/edicoes_anteriores_include.php?combo_data={month}/{year}'
            self.driver.get(website)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            times = [t['href'] for t in soup.find_all('a', href=True) if 'DATA' in t['href']]
            for t in times:
                file_t = t.split("=")[-1]
                filename = f"OSul{file_t}.pdf"
                if filename not in os.listdir():
                    response = requests.get(t,headers=self.headers)
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

    # The following method will download from one month to another later month
    def download_d1_d2(self,d1:tuple,d2:tuple):
        d1,d2 = self.compare(d1,d2)
        while d1 != d2:
            print(d1)
            self.download_month(d1)
            if d1[0] == 12:
                x = 1
                y = d1[1] + 1
                d1 = x, y
            else:
                x = d1[0] + 1
                y = d1[1]
                d1 = x, y
        if d1 == d2:
            print(d1)
            self.download_month(d1)

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(self.first_month,self.last_month)

    # The following method will check from one month to another later month
    def check_d1_d2(self,d1:tuple,d2:tuple):
        d1, d2 = self.compare(d1, d2)
        while d1 != d2:
            print(d1)
            self.check_month(d1)
            if d1[0] == 12:
                x = 1
                y = d1[1] + 1
                d1 = x, y
            else:
                x = d1[0] + 1
                y = d1[1]
                d1 = x, y
        if d1 == d2:
            print(d1)
            self.check_month(d1)

    # The following method will check all the dates on the archive
    def check_all(self):
        self.check_d1_d2(self.first_month,self.last_month)


    # The following method will compare
    def compare(self, d1: tuple, d2: tuple):
        if d1[1] < 2006:
            d1 = self.first_month

        if d2[1] < 2006:
            d2 = self.first_month

        if d2[1] > self.last_month[1]:
            d2 = self.last_month

        if d1[1] > self.last_month[1]:
            d1 = self.last_month

        if d1 not in self.months:
            d1 = self.last_month

        if d2 not in self.months:
            d2 = self.last_month

        if d1[0] > 12:
            x = 12
            y = d1[1]
            d1 = x, y

        if d2[0] > 12:
            x = 12
            y = d2[1]
            d1 = x, y

        if d1[1] > d2[1]:
            return d2, d1

        if d1[1] < d2[1]:
            return d1, d2

        if d1[0] > d2[0]:
            return d2, d1
        return d1, d2

if __name__ == "__main__":
    osul = OSul()
    osul.check_month((1,2025))


