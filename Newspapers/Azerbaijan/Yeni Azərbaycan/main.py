#Yeni Azərbaycan pdf downloader
#Newspaper from Azerbaijan
import selenium


from bs4 import BeautifulSoup
import requests,lxml

class YeniAzerbaycan:
    def __init__(self):
        self.main_page = "https://www.yeniazerbaycan.com/PDFxeber_1_az.html"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        self.links = []
        self.get_all()

    #This will find all the newspapers on the archive
    def get_all(self):
        main_page = "https://www.yeniazerbaycan.com/PDFxeber_1_az.html"

        html_content = requests.get(url=main_page,headers=self.headers)
        soup = BeautifulSoup(html_content.text, "lxml")

        last_page = [link["href"] for link in soup.find_all("a", href=True) if link.text == "Son"][0]
        last_page = int(last_page.split('_')[1])
        for i in range(1,last_page+1):
            page = f"https://www.yeniazerbaycan.com/PDFxeber_{i}_az.html"

            html_content = requests.get(url=page, headers=self.headers).text
            soup = BeautifulSoup(html_content, "lxml")

            links = [link["href"].replace(" ","%20") for link in soup.find_all("a",href=True) if ".pdf" in link["href"]]

            for link in links[:-2]:
                self.links.append(f"https://www.yeniazerbaycan.com/{link}")
                print(f"https://www.yeniazerbaycan.com/{link}")

    #This method will download the newspaper
    def download(self,download_link:str):
        response = requests.get(url=download_link,headers=self.headers)

        pdf_name = download_link.split("/")[-1]


        if response.status_code == 200:
            with open(f"{pdf_name}","wb") as f:
                f.write(response.content)
            with open("download_results.txt", "a") as f:
                f.write(f"{pdf_name} was downloaded\n")
            print(f"{pdf_name} was downloaded")
        else:
            with open("download_results.txt", "a") as f:
                f.write(f"{pdf_name} was not downloaded, it had response status code {response.status_code}\n")
            print(f"{pdf_name} was not downloaded, it had response status code {response.status_code}")

    #This method will download all the archive
    def download_all(self):
        for link in self.links[::-1]:
            link = link.replace("%20"," ")
            self.download(link)

    #This will download the latest newspaper found on the archive
    def download_latest(self):
        link = self.links[0]
        self.download(link)


if __name__ == "__main__":
    ya = YeniAzerbaycan()
