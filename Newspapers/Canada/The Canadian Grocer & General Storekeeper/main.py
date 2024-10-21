# The Canadian Grocer & General Storekeeper Archive

import requests,lxml
from bs4 import BeautifulSoup

class CanadianGrocerGeneralStorekeeper:
    def __init__(self):
        self.main_page = "https://www.canadiana.ca/view/oocihm.8_06959"
        self.links = self.get_links()


    def get_links(self)->list:
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        links = [(link['href'],link.text) for link in soup.find_all("a",class_="stretched-link")]
        return links

    def print_links(self):
        print(self.links)

    # The
    def download_index(self,index:int):
        paper_tuple= self.links[index]
        link = paper_tuple[0]
        filename = paper_tuple[1]

        pdf_soup = BeautifulSoup(requests.get(url=link).text,'lxml')
        link = pdf_soup.find("a",id='pvDownloadFull')
        link = link['href']

        response = requests.get(url=link)

        if response.status_code == 200:
            with open(f"{filename}.pdf","wb") as f:
                f.write(response.content)
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was downloaded\n")
            print(f"{filename} was downloaded")
        else:
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
            print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    #The following method will download the entire archive
    def download_all(self):
        for i in range(len(self.links)):
            self.download_index(i)


if __name__ == "__main__":
    cggs = CanadianGrocerGeneralStorekeeper()
    cggs.download_all()
