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
        self.years= [option.text for option in select_tag.find_all("option")]
        self.years = self.years[::-1]

    #This method will show all the years that you can choose from to download for the download_year method
    def show_years(self):
        print(self.years)

    #This method downloads all the magazines for that year is that year is on the website
    #the input year should be a string
    #example usage: k.download_year(year="1999")
    def download_year(self,year:str):
        if year in self.years:
            website = f"https://newspaper.kultura.bg/bg/archive/view/{year}"
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            links = [link['href'] for link in soup.find_all("a",href=True) if "htm" not in link["href"] and "https://newspaper.kultura.bg/bg/home/view/" in link["href"]]
            os.makedirs(year)

            for link in links:
                link_soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                pdf_link = link_soup.find("a",target=True,class_="pdf")["href"]

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
        lower_year = int(self.years[0])
        upper_year = int(self.years[-1])
        for year in range(lower_year,upper_year+1):
            website = f"https://newspaper.kultura.bg/bg/archive/view/{year}"
            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            links = [link['href'] for link in soup.find_all("a", href=True) if
                     "htm" not in link["href"] and "https://newspaper.kultura.bg/bg/home/view/" in link["href"]]
            os.makedirs(str(year))

            for link in links:
                link_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
                pdf_link = link_soup.find("a", target=True, class_="pdf")["href"]

                response = requests.get(url=pdf_link)
                filename = pdf_link.split("/")[-1]

                if response.status_code == 200:
                    with open(f"{year}/{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was downloaded\n")
                        print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was downloaded,it had response status code {response.status_code}")


if __name__ == "__main__":
    k = Kultura()

    #This method will download all the years on the website
    #Takes no input
    #k.download_years()

    #This method will show all the years that you can choose from
    #Takes no input
    #k.show_years()

    #This method will download all the pdfs in a year found on the website
    #the year has to be a string
    #k.download_year(year="1999")

