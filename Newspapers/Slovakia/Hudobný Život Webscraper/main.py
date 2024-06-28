#Webscraping a music magazine called Hudobný Život (it means musical life in slovak) from Slovakia

import requests,os
from bs4 import BeautifulSoup


class HudobnyZivot:
    def __init__(self):
        self.soup = BeautifulSoup(requests.get(url="https://hž.hc.sk").text,"lxml")
        self.years = [anchor.text for anchor in self.soup.find_all("a",href=True) if "#rok" in anchor["href"]]
        self.name = "Hudobný Život"

    #This method will download all the pdfs found on the website
    #It takes no input
    def download_all(self):
        pdfs = [f"https://hž.hc.sk/{anchor['href']}" for anchor in self.soup.find_all("a",href=True) if ".pdf" in anchor["href"]]
        os.makedirs(self.name)

        for pdf in pdfs:
            response = requests.get(url=pdf)
            filename = pdf.split("/")[-1]
            if response.status_code == 200:
                with open(f"{self.name}/{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded, it had response status code {response.status_code}")


    #This method will download any year that is on the website
    #the input of the year should be a string
    def download_year(self,year:str):
        if year in self.years:
            pdfs = [f"https://hž.hc.sk/{anchor['href']}" for anchor in self.soup.find_all("a", href=True) if".pdf" in anchor["href"] and year in anchor["href"]]
            os.makedirs(year)
            for pdf in pdfs:
                response = requests.get(url=pdf)
                filename = pdf.split("/")[-1]
                if response.status_code == 200:
                    with open(f"{year}/{filename}", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt", "a") as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")


if __name__ == "__main__":
    hz = HudobnyZivot()
    hz.download_year(year="1999")
    #hz.download_year(year="2020") example usage to download all the pdfs in 2020
    #hz.download_all() example usage to download all the pdfs found on the website