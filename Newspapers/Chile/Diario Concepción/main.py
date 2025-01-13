# Diario Concepción is a newspaper in Chile

import requests,datetime,lxml,os
from bs4 import BeautifulSoup


class DiarioConcepcion:
    def __init__(self):
        self.first_day = datetime.datetime(day=2,month=1,year=2017)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)


    #This method will return today's date
    def return_today(self)->datetime.datetime:
        today = datetime.datetime.today()
        time = datetime.datetime(day=today.day,month=today.month,year=today.year)
        return time


    # This method will download all the dates newspapers from one given date to another given date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(date=d1)
            d1 += self.one_day


    # This method will download the entire archive from the 2nd January 2017 till today
    def download_all(self):
        d1 = self.first_day
        d2 = self.today

        self.download_d1_d2(d1,d2)


    #This method will download today's Diario Concepción
    def download_latest(self):
        self.download_date(date=self.today)

    # This method will download a given specific date
    def download_date(self, date: datetime.datetime):
        if self.first_day <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            formatted_date = f"{day}-{month}-{year}"
            print(formatted_date)

            website = f"https://www.diarioconcepcion.cl/edicionimpresa/year/{year}/month/{month}/day/{day}"

            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            link = soup.find("a", href=True, target=True)

            try:
                os.mkdir(str(year))
            except FileExistsError:
                pass

            # This if statement will check if there was a copy released that day
            if link is None:
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} had no copy on the archive\n")
                print(f"{formatted_date} had no copy on the archive")
            else:
                # This will check which method should be used to download the newspaper
                if "assets" not in link["href"]:
                    link = f"https://www.diarioconcepcion.cl{link['href']}"

                    soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                    links = []
                    for link in soup.find_all("a",href=True):
                        if link["href"] == "#":
                            try:
                                url = link["data-full"]
                                url = url.split("-")
                                url.pop()
                                url = "-".join(url)
                                url += ".jpg"
                                links.append(url)

                            except KeyError:
                                continue
                    self.download_links(formatted_date,year,links)
                else:
                    link = link["href"]
                    self.download_pdf_link(link,formatted_date,year)


    # This method will download a group of image links given to it
    def download_links(self,formatted_date:str,year:int,links:list):
        path = f"{year}/{formatted_date}"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        for i in range(len(links)):
            page_number = i+1

            pdf = links[i]
            response = requests.get(pdf)

            if response.status_code == 200:
                with open(f"{path}/{page_number}.jpg","wb") as f:
                    f.write(response.content)

                with open("download_results.txt","a") as f:
                    f.write(f"{path}/{page_number}.jpg was downloaded\n")
                print(f"{path}/{page_number}.jpg was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{path}/{page_number}.jpg was not downloaded,it had response status code {response.status_code}\n")
                print(f"{path}/{page_number}.jpg was not downloaded,it had response status code {response.status_code}")


    # This method will download the pdf link
    def download_pdf_link(self,link:str,formatted_date:str,year:int):
        response = requests.get(url=link)
        if response.status_code == 200:
            with open(f"{year}/{formatted_date}.pdf", "wb") as f:
                f.write(response.content)

            with open("download_results.txt", "a") as f:
                f.write(f"{formatted_date} was downloaded\n")
            print(f"{formatted_date} was downloaded")
        else:
            with open("download_results.txt", "a") as f:
                f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
            print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")

    # The following method will check if the pdf for a particular date has been downloaded or not
    def check_date(self,date: datetime.datetime):
        if self.first_day <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            formatted_date = f"{day}-{month}-{year}"
            print(formatted_date)

            website = f"https://www.diarioconcepcion.cl/edicionimpresa/year/{year}/month/{month}/day/{day}"

            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            link = soup.find("a", href=True, target=True)

            try:
                os.mkdir(str(year))
            except FileExistsError:
                pass

            # This if statement will check if there was a copy released that day
            if link is None:
                with open("download_results.txt","a") as f:
                    f.write(f"{formatted_date} had no copy on the archive\n")
                print(f"{formatted_date} had no copy on the archive")
            else:
                # This will check which method should be used to download the newspaper
                if "assets" not in link["href"]:
                    link = f"https://www.diarioconcepcion.cl{link['href']}"

                    soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                    links = []
                    for link in soup.find_all("a",href=True):
                        if link["href"] == "#":
                            try:
                                url = link["data-full"]
                                url = url.split("-")
                                url.pop()
                                url = "-".join(url)
                                url += ".jpg"
                                links.append(url)

                            except KeyError:
                                continue
                    self.check_download_links(formatted_date,year,links)
                else:
                    link = link["href"]
                    self.check_download_pdf_link(link,formatted_date,year)

    # This method will check a group of image links given to it to see if they have been downloaded or not
    def check_download_links(self,formatted_date:str,year:int,links:list):
        path = f"{year}/{formatted_date}"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        for i in range(len(links)):
            page_number = i+1
            pdf = links[i]
            if f"{page_number}.jpg" not in os.listdir(path):
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"{path}/{page_number}.jpg","wb") as f:
                        f.write(response.content)

                    with open("download_results.txt","a") as f:
                        f.write(f"{path}/{page_number}.jpg was downloaded\n")
                    print(f"{path}/{page_number}.jpg was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{path}/{page_number}.jpg was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{path}/{page_number}.jpg was not downloaded,it had response status code {response.status_code}")

    # This method will check if the pdf link has been downloaded or not. If it has not been downloaded it will get downloaded
    def check_download_pdf_link(self,link:str,formatted_date:str,year:int):
        if f"{formatted_date}.pdf" in os.listdir(str(year)):
            response = requests.get(url=link)
            if response.status_code == 200:
                with open(f"{year}/{formatted_date}.pdf", "wb") as f:
                    f.write(response.content)

                with open("download_results.txt", "a") as f:
                    f.write(f"{formatted_date} was downloaded\n")
                print(f"{formatted_date} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{formatted_date} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{formatted_date} was not downloaded,it had response status code {response.status_code}")

    # This method will check all the dates newspapers from one given date to another given date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(date=d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        d1 = self.first_day
        d2 = self.today
        self.check_d1_d2(d1,d2)


if __name__ == "__main__":
    dc = DiarioConcepcion()

    # The following method will download all the Diario Concepción papers from the 28th August 2024 till today
    # d1 = datetime.datetime(day=28,month=8,year=2024)
    # d2 = dc.today
    #dc.download_d1_d2(d1,d2)

    # The following method will download the Diario Concepción paper for the 28th August 2024
    # dc.download_date(d1)

    # The following method will download the entire archive
    # from the start date of 2nd January 2017 till today
    # dc.download_all()

    # The following method will download today's copy of Diario Concepción
    # dc.download_latest
