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
        duma = "Duma"
        os.makedirs(duma)
        while self.initial_date <= self.final_date:
            day = self.initial_date.day
            month = self.initial_date.month
            year = self.initial_date.year
            website = f"https://duma.bg/?go=newspaper&p=list&year={year}&month={month}&day={day}"

            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            try:
                pdf_link = soup.find("a",href=True,class_="dwnl_newspaper_item")["href"]
            except TypeError:
                pass
            else:
                pdf_link = "https://duma.bg/" + pdf_link
                filename = f"{day}-{month}-{year}.pdf"

                response = requests.get(url=pdf_link)
                if response.status_code == 200:
                    with open(f"{duma}/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt",'a') as f:
                        f.write(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                    print(f"{filename}  was not downloaded, it had status code {response.status_code}\n")

            self.initial_date += self.one_day

    #This will download any year between 2009 and the year that we are currently in
    def download_year(self,year:int):
        os.makedirs(str(year))
        if year >= 2009:
            initial_date = datetime.datetime(day=1,month=1,year=year)
            final_date = datetime.datetime(day=31,month=12,year=year)
            while initial_date <= final_date:
                print(initial_date)
                day = initial_date.day
                month = initial_date.month
                year = initial_date.year
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
                        with open(f"{year}/{filename}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", 'a') as f:
                            f.write(f"{filename} was downloaded\n")
                        print(f"{filename} was downloaded")
                    else:
                        with open("download_results.txt", 'a') as f:
                            f.write(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                initial_date += self.one_day

    #tuple(day,month,year)
    #lets say you want to download from 9th march 2018 til 15th september 2019
    #download(date1=(9,3,2018),date2=(15,9,2019)) is an example usage of the following method
    def download(self,date1:tuple,date2:tuple):
        initial_date = datetime.datetime(day=date1[0], month=date1[1], year=date1[2])
        final_date = datetime.datetime(day=date2[0], month=date2[1], year=date2[2])
        year = date1[2]
        if year >= 2009:
            if initial_date < final_date:
                name = "Duma Downloads"
                os.makedirs("Duma Downloads")
                while initial_date <= final_date:
                    print(initial_date)
                    day = initial_date.day
                    month = initial_date.month
                    year = initial_date.year
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
                            with open(f"{name}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", 'a') as f:
                                f.write(f"{filename} was downloaded\n")
                            print(f"{filename} was downloaded")
                        else:
                            with open("download_results.txt", 'a') as f:
                                f.write(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                            print(f"{filename} was not downloaded, it had status code {response.status_code}\n")
                    initial_date += self.one_day

    #This will download the newspaper for today
    def download_today(self):
        day = self.final_date.day
        month = self.final_date.month
        year = self.final_date.year
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


