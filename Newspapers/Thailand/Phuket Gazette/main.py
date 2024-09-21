#Phuket Gazette was a weekly english newspaper published in Phuket,Thailand
#https://en.wikipedia.org/wiki/Phuket_Gazette is the wikipedia link 

import requests,lxml,os
from bs4 import BeautifulSoup



class PhuketGazette:
    def __init__(self):
        self.website = "https://thethaiger.com/digital-gazette"
        self.soup = BeautifulSoup(requests.get(url=self.website).text,"lxml")
        self.years = []
        self.find_years()


    # This method will find all the years on the website for the pdfs
    def find_years(self):
        self.years = [int(year.text) for year in self.soup.find_all("h4")]

    # This method will download a specific year
    def download_year(self,year:int):
        if year in self.years:
            pdfs = [link["href"] for link in self.soup.find_all("a",href=True) if str(year) in link["href"]]
            pdfs = sorted(pdfs)

            os.mkdir(str(year))
            for pdf in pdfs:
                response = requests.get(url=pdf)
                filename = pdf.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{year}/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # This method will download all the pdfs from one year to another
    # download_year1_year2(2010,2015) will download 2010,2011,2012,2013,2014,2015
    def download_year1_year2(self,year1:int,year2:int):
        for year in range(year1,year2+1):
            self.download_year(year)


    # his method will download all the pdfs on the website
    def download_all(self):
        first_year = min(self.years)
        last_year = max(self.years)
        self.download_year1_year2(first_year,last_year)



if __name__ == "__main__":
    pg = PhuketGazette()

    # The following method use will download all the newspapers
    # pg.download_all()

    # The following method use will download a specific year as mentioned.In this case it will download 2015
    # pg.download_year(2015)

    # The following method use will download a specific year as mentioned.In this case it will download all the years from 2010 to 2012
    # pg.download_year1_year2(2010,2012)

