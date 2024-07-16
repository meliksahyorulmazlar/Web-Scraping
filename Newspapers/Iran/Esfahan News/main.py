#Esfahan News pdf Webscraper
import requests,lxml
from bs4 import BeautifulSoup


class EsfahanNews:
    def __init__(self):
        self.year_links = []
        self.year_dictionary = {}
        self.pdf_links = []
        self.get_years()

    #This method will find the years on the website
    def get_years(self):
        main_page = "https://www.esfahan-news.com"
        if len(self.year_links) == 0:
            soup = BeautifulSoup(requests.get(url=main_page).text, "lxml")
            for link in soup.find_all('a', href=True):
                if ".html" in link["href"] and link["href"] not in self.year_links:
                    self.year_links.append(link["href"])


            self.year_links = self.year_links[::-1]
            for year in self.year_links:
                year_link = year
                year = (year.split("/")[-1]).strip(".html")
                if len(year) == 2:
                    year = f"13{year}"
                    self.year_dictionary[year] = year_link
                else:
                    self.year_dictionary[year] = year_link

    #This method will download a link
    def download_link(self,download_link:str):
        response = requests.get(url=download_link)
        filename = download_link.split("/")[-1]

        if response.status_code == 200:
            with open(f"{filename}","wb") as f:
                f.write(response.content)
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was downloaded\n")
            print(f"{filename} was downloaded")
        else:
            with open("download_results.txt","a") as f:
                f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
            print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    #This method will find the pdfs found on that page
    def find_pdfs(self,year_link:str)->list:
        soup = BeautifulSoup(requests.get(url=year_link).text,"lxml")
        pdf_links = [link["href"] for link in soup.find_all("a", href=True) if "pdf" in link["href"]]
        pdf_links = sorted(pdf_links, key=lambda x: int((x.split("/")[-1]).replace("no.pdf", "")))
        return pdf_links

    #This method will download all the pdfs found on the website
    def download_all(self):
        for year in self.year_dictionary:
            links = self.find_pdfs(year_link=self.year_dictionary[year])
            for link in links:
                self.download_link(link)
    #This method will download a year on the website
    #1399 in the persian calender will work
    #Example usage
    #en = EsfahanNews()
    #en.download_year(year="1399")
    def download_year(self,year:str):
        if year in self.year_dictionary:
            links = self.find_pdfs(year_link=self.year_dictionary[year])
            for link in links:
                self.download_link(link)
        else:
            print("Year not found")

    #This will download the latest pdf
    def download_latest(self):
        last_link = self.year_links[-1]
        links = self.find_pdfs(year_link=last_link)
        link = links[-1]
        self.download_link(download_link=link)

    #if n1 is 500 , n2 = 505
    #it will download 500no.pdf 501no.pdf 502no.pdf 503no.pdf 504no.pdf 505no.pdf
    def download_n1_n2(self,n1:int,n2:int):
        if n2 < n1:
            c = n1
            n1 = n2
            n2 = c

        all_links = []
        for year in self.year_dictionary:
            all_links += self.find_pdfs(year_link=self.year_dictionary[year])

        for link in all_links:
            link_number = int((link.split("/")[-1]).strip("no.pdf"))
            if n1 <= link_number <=n2:
                self.download_link(download_link=link)



if __name__ == "__main__":
    en = EsfahanNews()
    en.download_all()
