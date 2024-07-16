#Vatan-e Emrooz pdf webscraper
#Vatan-e Emrooz is a newspaper in Iran


import requests,lxml,os
from bs4 import BeautifulSoup

class VataneEmrooz:
    def __init__(self):
        self.latest = self.find_latest()

    #This method will find the latest number of Vatan-e Emrooz
    def find_latest(self)->int:
        website = "https://vatanemrooz.ir"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        for link in soup.find_all("a",href=True):
            if "nid" in link["href"]:
                number = int(link["href"].split("=")[1].strip("&pnid"))
                return number

    #This method will download nth newspaper of Vatan-e Emrooz
    def download(self,number:int):
        i = number
        website = f"https://vatanemrooz.ir/?nid={i}&pid=1&type=0"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        try:
            day = soup.find("div", class_="newspaperdate").text
        except AttributeError:
            pass
        else:
            filename = day + f" {i}"
            os.makedirs(filename)
            pdfs = [f"https://vatanemrooz.ir{link['href']}" for link in soup.find_all("a", href=True) if "PagePDF" in link["href"] and "AllPagePDF" not in link['href']]
            for pdf in pdfs:
                response = requests.get(url=pdf)
                if response.status_code == 200:
                    with open(f"{filename}/{pdfs.index(pdf) + 1}.pdf", "wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{i}/{pdfs.index(pdf) + 1}.pdf was downloaded\n")
                    print(f"{i}/{pdfs.index(pdf) + 1}.pdf was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{i}/{pdfs.index(pdf) + 1}.pdf was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{i}/{pdfs.index(pdf) + 1}.pdf was not downloaded,it had response status code {response.status_code}")


    #This will download all the newspapers of Vatan-e Emrooz
    def download_all(self):
        for i in range(1,self.latest+1):
            self.download(i)

    #This will download the latest newspaper of Vatan-e Emrooz
    def download_latest(self):
        self.download(number=self.latest)


    #This will download all the newspapers of Vatan-e Emrooz from the n1th newspaper till the n2nd newspaper
    #download_n1_n2(1,5)
    #will download 1,2,3,4,5 of Vatan-e Emrooz
    def download_n1_n2(self,n1,n2):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            self.download(i)


if __name__ == "__main__":
    ve = VataneEmrooz()
    ve.download_n1_n2(4000,4005)
