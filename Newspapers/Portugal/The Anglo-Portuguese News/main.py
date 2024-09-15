#The Anglo Portuguese News was founded in 1937 by Major C. E. Wakeham, with Luiz Marques as editor.
#It was the only English language newspaper published right through the Second World War in continental Europe, 
#and the German broadcasting system referred to the paper as "Churchill's mouthpiece in Lisbon", which was a source of great pride to the editor.

#Luiz Marques purchased the paper in 1954 and from then on was proprietor and editor until his death in October 1976.
#His wife Susan Lowndes Marques, who had written for the newspaper since 1954, assumed the role of proprietor and editor after her husband's death 
#and sold the paper to Nigel Batley in 1980.

#From 1937 until its closure in 2004, The Anglo-Portuguese News served as a record for the British 
#and other foreign communities in Portugal as well as publishing articles by local residents and topographical pieces on Portugal,
#and is an invaluable resource for researchers and anyone writing about the British community and institutions in Portugal.

import requests,lxml
from bs4 import BeautifulSoup


class AngloPortugueseNews:
    def __init__(self):
        self.start_month_year:tuple = 2,1937
        self.end_month_year:tuple = 2,2004
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
        self.main = "https://www.angloportuguesenews.pt"

    def download_month(self,month:int,year:int)->None:
        if month < 10:
            month = f"0{month}"

        website = f"https://www.angloportuguesenews.pt/?a=cl&cl=CL2.{year}.{month}&e=-------en-20--1--txt-txIN-------"

        response = requests.get(url=website,headers=self.headers)
        soup = BeautifulSoup(response.text,"lxml")
        pdfs = [f'{self.main}{link["href"]}' for link in soup.find_all("a",href=True) if "APN" in link["href"]]
        if len(pdfs) == 0:
            print("There were no pdfs")
        else:
            for pdf in pdfs:
                print(pdfs)
                items = pdf.split("=")
                item = items[2].strip("&e")

                pdf_page = f"https://www.angloportuguesenews.pt/?a=is&oid={item}&type=staticpdf&e=-------en-20--1--txt-txIN-------"

                response = requests.get(pdf_page,headers=self.headers)
                if response.status_code == 200:
                    with open(f"{item}.pdf","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{item} was downloaded\n")
                    print(f"{item} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{item} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{item} was not downloaded, it had response status code {response.status_code}\n")

    #This method will download from 1 specific month to another
    def download_d1_d2(self,d1:tuple,d2:tuple):
        d1_month = d1[0]
        d1_year = d1[1]

        d2_month = d2[0]
        d2_year = d2[1]


        while not ((d1_month == d2_month) and (d1_year == d2_year)):
            print(d1_month, d1_year)
            month = d1_month
            year = d1_year

            self.download_month(month,year)

            if month == 12:
                d1_month = 1
                d1_year += 1
            else:
                d1_month += 1


    #This method will download the entire archive from 1937 to 2004
    def download_all(self):
        self.download_d1_d2(d1=(2,1937),d2=(2,2004))


if __name__ == "__main__":
    apn = AngloPortugueseNews()
    apn.download_d1_d2(d1=(3,1961),d2=apn.end_month_year)
     
