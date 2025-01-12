#Kultura Webscraper.Kultura is a Bulgarian magazine(In Bulgarian, Kultura means culture)
import requests,os,lxml
from bs4 import BeautifulSoup

class Kultura:
    def __init__(self):
        self.links = []
        self.years = []
        self.get_years()


    #This will find all the years on the website
    def get_years(self):
        website = f"https://newspaper.kultura.bg/bg/archive/view/"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        select_tag = soup.find("select",class_="one_option",id="archive_year")
        self.years= [int(option.text) for option in select_tag.find_all("option")]
        self.years = self.years[::-1]

    #This method will show all the years that you can choose from to download for the download_year method
    def show_years(self):
        print(self.years)

    #This method downloads all the magazines for that year is that year is on the website
    #the input year should be an integer
    #example usage: k.download_year(year="1999")
    def download_year(self,year:int):
        if year in self.years:
            website = f"https://newspaper.kultura.bg/bg/archive/view/{year}"
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            links = [link['href'] for link in soup.find_all("a",href=True) if "htm" not in link["href"] and "https://newspaper.kultura.bg/bg/home/view/" in link["href"]]
            os.makedirs(str(year))
            print(links)
            for link in links:
                link_soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                pdf_link = link_soup.find("a",target=True,class_="pdf")

                #This if statement will check if there is a pdf or not
                if pdf_link is not None:
                    pdf_link = pdf_link["href"]
                    #https://newspaper.kultura.bg/media/file/{}<-- name of the pdf within those curly braces

                    response = requests.get(url=pdf_link)
                    filename = pdf_link.split("/")[-1]

                    if response.status_code == 200:
                        with open(f"{year}/{filename}","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{filename} was downloaded\n")
                            print(f"{filename} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{filename} was downloaded,it had response status code {response.status_code}")

    #This method will download all the years on the website
    #It takes no input
    def download_years(self):
        first_year = self.years[0]
        last_year = self.years[1]
        self.download_year1_year2(year1=first_year,year2=last_year)

    #This will download all the pdfs from one specified year to another
    def download_year1_year2(self,year1:int,year2:int):
        if year1 > year2:
            c = year1
            year1 = year2
            year2 = c
        for year in range(year1,year2+1):
            self.download_year(year)

    # The following method will check if the pdfs for a particular year have been downloaded or not
    def check_year(self,year:int):
        if year in self.years:
            website = f"https://newspaper.kultura.bg/bg/archive/view/{year}"
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            links = [link['href'] for link in soup.find_all("a",href=True) if "htm" not in link["href"] and "https://newspaper.kultura.bg/bg/home/view/" in link["href"]]
            os.makedirs(str(year))
            print(links)
            for link in links:
                link_soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                pdf_link = link_soup.find("a",target=True,class_="pdf")

                #This if statement will check if there is a pdf or not
                if pdf_link is not None:
                    pdf_link = pdf_link["href"]
                    #https://newspaper.kultura.bg/media/file/{}<-- name of the pdf within those curly braces


                    filename = pdf_link.split("/")[-1]
                    if filename not in os.listdir(f"{year}"):
                        response = requests.get(url=pdf_link)
                        if response.status_code == 200:
                            with open(f"{year}/{filename}","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{filename} was downloaded\n")
                                print(f"{filename} was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{filename} was downloaded,it had response status code {response.status_code}")

    #The following method will check from one particular year to another particular year
    def check_year1_year2(self,year1:int,year2:int):
        if year1 > year2:
            c = year1
            year1 = year2
            year2 = c
        for year in range(year1,year2+1):
            self.check_year(year)

    #This method will check if all the pdfs have been downloaded or not
    def check_years(self):
        first_year = min(self.years)
        last_year = max(self.years)
        self.check_year1_year2(first_year,last_year)


if __name__ == "__main__":
    k = Kultura()

    #This method will download all the years on the website
    #Takes no input
    #k.download_years()

    #This method will show all the years that you can choose from to download
    #Takes no input
    #k.show_years()

    #This method will download all the pdfs in a year found on the website
    #the year has to be an integer
    #k.download_year(year=1999)

    #This method will download all the pdfs from one year to another
    #the two arguments have to be an integer
    #k.download_year1_year2(year1=1990,year2=2000) 
    #will download the following years:
    #1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000

