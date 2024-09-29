# The Diário de Lisboa was a daily evening newspaper
# published in the Portuguese capital of Lisbon between 1921 and 1990.

import requests,lxml,datetime,os,time
from bs4 import BeautifulSoup
from selenium import webdriver

class DiariodeLisboa:
    def __init__(self):
        self.start_date = datetime.datetime(day=2,month=5,year=1921)
        self.end_date = datetime.datetime(day=30,month=11,year=1990)
        self.one_day = datetime.timedelta(days=1)

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)



    # The following method will download a particular given date
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.end_date:
            try:
                os.mkdir(str(date.year))
            except FileExistsError:
                pass
            website = f"http://casacomum.org/cc/diario_de_lisboa/dia?ano={date.year}&mes={date.month}"
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            days = [int(span.text) for span in soup.find_all("span",class_="dia_do_mes_sobre")]

            if date.day in days:
                links = [self.replace_href(link["href"]) for link in soup.find_all("a",href=True)]
                links = links[6:]
                index = days.index(date.day)
                link = links[index]
                print(link)
                self.get_images(date,link)
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{date.day}-{date.month}-{date.year} is not on the archive\n")
                print(f"{date.day}-{date.month}-{date.year} is not on the archive")
        else:
            with open("download_results.txt", "a") as f:
                f.write(f"{date.day}-{date.month}-{date.year} is a date either before the archive began or after it finished\n")
            print(f"{date.day}-{date.month}-{date.year} is a date either before the archive began or after it finished")

    # The following method when given a link will find all the images
    def get_images(self,date:datetime.datetime,link:str):
        soup = BeautifulSoup(requests.get(url=link).text,"lxml")
        spans = [int(span.text.replace("/","").strip()) for span in soup.find_all("span") if "/" in span.text]
        page_count = spans[0]

        soup = BeautifulSoup(requests.get(url=link).text,"lxml")
        images = [image["src"] for image in soup.find_all("img",alt=True)]
        images = images[4:]
        images = [img.replace("d3","d2").replace("D3","D2").replace("jpg","png") for img in images]
        for i in range(len(images)):
            self.download_image(date,images[i],i+1)

    # The following method will download an image when given a link
    def download_image(self,date:datetime.datetime,image_link:str,count:int):
        response = requests.get(url=image_link)
        formatted_date = f"{date.day}-{date.month}-{date.year}"
        try:
            os.mkdir(f"{date.year}/{formatted_date}")
        except FileExistsError:
            pass
        if response.status_code == 200:
            with open(f"{date.year}/{formatted_date}/{count}.png","wb") as f:
                f.write(response.content)
            with open("download_results.txt", "a") as f:
                f.write(f"{date.year}/{formatted_date}/{count}.png was downloaded\n")
            print(f"{date.year}/{formatted_date}/{count}.png was downloaded")
        else:
            image_link = image_link.replace(".png", ".jpg")
            new_response = requests.get(url=image_link)
            if new_response.status_code == 200:
                with open(f"{date.year}/{formatted_date}/{count}.png", "wb") as f:
                    f.write(new_response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{date.year}/{formatted_date}/{count}.png was downloaded\n")
                print(f"{date.year}/{formatted_date}/{count}.png was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{date.year}/{formatted_date}/{count}.png was not downloaded,it had response status code {new_response.status_code}\n")
                print(f"{date.year}/{formatted_date}/{count}.png was not downloaded,it had response status code {new_response.status_code}")

    # The following method gets the link for the newspaper
    def replace_href(self,string:str):
        return f"http://casacomum.org/cc{string.replace('..','')}"

    # The following method will download all the dates from one date to another given date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(d1=self.start_date,d2=self.end_date)


if __name__ == "__main__":
    dl = DiariodeLisboa()

    # The following method use will download the images for the 5th May 1920
    dl.download_date(date=datetime.datetime(day=5,month=5,year=1920))

    # This method will download the entire archive
    dl.download_all()

    # The following method will download all the images from one date to another
    # It will end up downloading all the images from the 4th May 1921 till the 18th May 1921
    dl.download_d1_d2(d1=datetime.datetime(day=4,month=5,year=1921),d2=datetime.datetime(day=18,month=5,year=1921))





