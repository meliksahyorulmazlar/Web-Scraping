#The Antartic Sun Newspaper Archive

import requests,os,lxml
from bs4 import BeautifulSoup


class TheAntarticSun:
    def __init__(self):
        self.page = "https://antarcticsun.usap.gov/pastissues/archives.cfm"
        self.seasons = {}
        self.return_seasons()

    # This method will get all the seasons on the archive from 1996-1997
    def return_seasons(self):
        soup = BeautifulSoup(requests.get(url=self.page).text,"lxml")

        for link in soup.find_all("a",href=True):
            if "pastIssues" in link["href"] and link.text != "Past Issues":

                url = f"https://antarcticsun.usap.gov{link['href']}"
                season = link.text
                self.seasons[season] = url

        values = dict(sorted(self.seasons.items(), key=lambda x: x[0]))
        self.seasons = values

    # This method will print all the sessions on the archive
    def print_seasons(self):
        print([key[0] for key in self.seasons.items()])

    # The following method will download a particular method
    def download_season(self,season:str):
        if season in self.seasons:
            print(season)
            try:
                os.mkdir(season)
            except FileExistsError:
                pass

            url = self.seasons[season]
            soup = BeautifulSoup(requests.get(url).text,"lxml")
            pdfs = [f'https://antarcticsun.usap.gov{link["href"]}' for link in soup.find_all("a",href=True) if season in link["href"]]

            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                print(filename)

                response = requests.get(url=pdf)

                if response.status_code == 200:
                    with open(f"{season}/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")



    #This method will download all the seasons on the archive:
    def download_all(self):
        for season in self.seasons:
            self.download_season(season)



if __name__ == "__main__":
    tas = TheAntarticSun()
    tas.download_all()
