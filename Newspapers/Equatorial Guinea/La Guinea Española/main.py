#Webscraper download La Guinea Española a former newspaper that was once in Equatorial Guinea

import requests,os,lxml
from bs4 import BeautifulSoup


class GuineaEspanola:
    def __init__(self):
        self.website = "http://www.bioko.net/guineaespanola/laguies.htm"
        self.name = "La Guinea Española"
        self.soup = BeautifulSoup(requests.get(url=self.website).text,"lxml")
        self.links = [f'http://www.bioko.net/guineaespanola/{item["href"]}' for item in self.soup.find_all("a",href=True)if "A1" in item["href"]]
        self.years = [item["href"].strip("A").strip(".htm") for item in self.soup.find_all("a",href=True)if "A1" in item["href"]]

    # The following method will download a specific year
    def download_year(self,year:str):
        if year in self.years:
            website = f"http://www.bioko.net/guineaespanola/A{year}.htm"
            new_soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            pdf_links = [f'http://www.bioko.net/guineaespanola/{item["href"]}' for item in new_soup.find_all("a",href=True) if ".pdf" in item['href']]

            os.makedirs(year)
            for pdf in pdf_links:
                response = requests.get(url=pdf,timeout=10)
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

    # The following method will download all the years on the archive
    def download_all(self):
        os.makedirs(self.name)
        for year in self.years:
            website = f"http://www.bioko.net/guineaespanola/A{year}.htm"
            new_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            pdf_links = [f'http://www.bioko.net/guineaespanola/{item["href"]}' for item in new_soup.find_all("a", href=True) if ".pdf" in item['href']]

            for pdf in pdf_links:
                response = requests.get(url=pdf,timeout=10)
                filename = pdf.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{self.name}/{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will update/check the pdfs for a specific year
    def check_year(self,year:str):
        if year in self.years:
            website = f"http://www.bioko.net/guineaespanola/A{year}.htm"
            new_soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            pdf_links = [f'http://www.bioko.net/guineaespanola/{item["href"]}' for item in new_soup.find_all("a",href=True) if ".pdf" in item['href']]

            os.makedirs(year)
            for pdf in pdf_links:
                filename = pdf.split("/")[-1]
                if filename not in os.listdir(year):
                    response = requests.get(url=pdf,timeout=10)
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

    #The following method will update/check all the years on the archive
    def check_all(self):
        for year in self.years:
            self.check_year(year)


if __name__ == "__main__":
    ge = GuineaEspanola()
    #The following method downloads all of them
    #takes no input
    #ge.download_all()

    #This method download all the pdfs for that year
    #the year input has to be a string (any year from 1903 to 1969 except 1941,1942)
    #ge.download_year(year="1955")
