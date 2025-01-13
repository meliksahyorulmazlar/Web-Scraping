#A newspaper archive webscraper from Turkey
#The website is https://www.gastearsivi.com
# The following newspapers are included in the archive.
# If a newspaper name ends with "Yeni" (which means "new" in Turkish),
# it indicates that this is the newer version of that newspaper.
# List of newspapers:
# ['Ağaç', 'Ahali (Filibe)', 'Akis', 'Akşam', 'Anadolu', 'Aydede', 'Balkan (Filibe)', 'Birgün', 'Bugün', 'Bugün Yeni',
# 'Büyük Doğu', 'Commodore', 'Cumhuriyet', 'Diyojen', 'Haber', 'Hakimiyet-i Milliye', 'Halkın Sesi', 'Hayat', 'Her Ay',
# 'İkaz (Afyonkarahisar)', 'İkdam (Sabah Postası)', 'İrade-i Milliye (Sivas)', 'Kadro', 'Kurun', 'Milli Gazete',
# 'Milliyet', 'Peyam', 'Radikal', 'Sebilürreşad', 'Serbes Cumhuriyet', 'Servet', 'Servet-i Fünun', 'Servetifunun (Uyanış)',
# 'Son Posta', 'Son Telgraf', 'Sözcü', 'Takvim-i Vekayi', 'Tan', 'Tanin', 'Tanin Yeni', 'Taraf', 'Tasviri Efkar', 'Türk Dili',
# 'Ulus', 'Ulusal Birlik (İzmir)', 'Vakit', 'Vatan', 'Yarım Ay', 'Yarın', 'Yeni Asır', 'Yenigün (Antakya)', 'Yeni İstanbul',
# 'Yeni Sabah', 'Yeni Şafak', 'Zafer', 'Zaman', 'Zaman Yeni']
import webbrowser

import requests,os,lxml
from bs4 import BeautifulSoup


class GasteArsivi:
    def __init__(self):
        self.main_page = "https://www.gastearsivi.com"
        self.newspapers = []
        self.newspaper_links = []
        self.get_newspapers()

    #This will decode some unrecognizable text to get the Turkish text
    def decode_turkish(self,turkish_text:str):
        replacements = {'Ã§': 'ç','Ã¶': 'ö','Ã¼': 'ü','Ä\x9f': 'ğ','Ä±':'ı','Å\x9f': 'ş','Ä°': 'İ',"Å\x9e":"Ş",}
        for replacement in replacements:
            if replacement in turkish_text:
                turkish_text = turkish_text.replace(replacement,replacements[replacement])
        return turkish_text

    #
    def get_newspapers(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text,"lxml")
        self.newspaper_links = [f'https://www.gastearsivi.com{self.decode_turkish(turkish_text=link["href"])}' for link in soup.find_all("a",href=True,class_="StyledComponents__StyledLink-sc-1vz7aia-18 IndexComponent__SayfaLink-gcqg9b-0 hBkgwa bNPNEp h-100 d-flex flex-column")]
        for link in soup.find_all("a", href=True,class_="StyledComponents__StyledLink-sc-1vz7aia-18 IndexComponent__SayfaLink-gcqg9b-0 hBkgwa bNPNEp h-100 d-flex flex-column"):
            newspaper = self.decode_turkish(turkish_text=link.text)
            if newspaper in self.newspapers:
                newspaper = f"{newspaper} Yeni"
            self.newspapers.append(newspaper)

    #This will show all the indices of the newspapers
    #important to download a single newspaper for the download_newspaper method
    def show_indices(self):
        newspapers = [(self.newspapers[i],i)for i in range(len(self.newspapers))]
        print(newspapers)


    #This method will download a specific newspaper that corresponds to its index
    #You can use the show_indices method to get to index of the newspaper you want to download
    #For example,if you want to download Ağaç for the index paramter you can enter 0 like this:
    #download_newspaper(index=0)
    def download_newspaper(self,index:int):
        if 0 <= index < len(self.newspapers):
            name = self.newspapers[index]
            os.makedirs(name)

            website = self.newspaper_links[index]
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            page_links = [number.text for number in soup.select("div nav ul li span")]
            number_of_pages = int(page_links[-1])
            newspaper_links = []

            #finding all the newspapers
            for i in range(1,number_of_pages+1):
                current_page = f"{website}/{i}"
                print(current_page)
                soup = BeautifulSoup(requests.get(url=current_page).text,"lxml")
                news_links = [f'https://www.gastearsivi.com{link["href"]}' for link in soup.find_all("a",href=True,itemprop=True) if link["itemprop"]=="mainEntityOfPage"]
                for new_link in news_links:
                    newspaper_links.append(new_link)

            #finding all the pages of the newspaper
            for link in newspaper_links:
                newspaper_date = link.split("/")[-2]
                os.makedirs(f"{name}/{newspaper_date}")

                paper_soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                pages = [f'https://www.gastearsivi.com{link["href"]}' for link in paper_soup.find_all("a",href=True,class_="StyledComponents__StyledLink-sc-1vz7aia-18 hBkgwa mr-1")]

                #downloading the pages
                for page in pages:

                    photo_soup = BeautifulSoup(requests.get(url=page).text,"lxml")
                    photo = photo_soup.find("img",src=True)["src"]
                    filename = photo.split("/")[-1]

                    response = requests.get(url=photo)


                    if response.status_code == 200:
                        with open(f"{name}/{newspaper_date}/{filename}","wb") as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{name}/{newspaper_date}/{filename} was downloaded\n")
                        print(f"{name}/{newspaper_date}/{filename} was downloaded")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{name}/{newspaper_date}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{name}/{newspaper_date}/{filename} was downloaded,it had response status code {response.status_code}")

    #This method will download all the newspapers
    def download_all(self):
        for i in range(len(self.newspapers)):
            self.download_newspaper(index=i)

    # The following method will check if all the newspapers for a newspaper were downloaded or not
    def check_newspaper(self,index:int):
        if 0 <= index < len(self.newspapers):
            name = self.newspapers[index]
            os.makedirs(name)

            website = self.newspaper_links[index]
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            page_links = [number.text for number in soup.select("div nav ul li span")]
            number_of_pages = int(page_links[-1])
            newspaper_links = []

            #finding all the newspapers
            for i in range(1,number_of_pages+1):
                current_page = f"{website}/{i}"
                print(current_page)
                soup = BeautifulSoup(requests.get(url=current_page).text,"lxml")
                news_links = [f'https://www.gastearsivi.com{link["href"]}' for link in soup.find_all("a",href=True,itemprop=True) if link["itemprop"]=="mainEntityOfPage"]
                for new_link in news_links:
                    newspaper_links.append(new_link)

            #finding all the pages of the newspaper
            for link in newspaper_links:
                newspaper_date = link.split("/")[-2]
                os.makedirs(f"{name}/{newspaper_date}")

                paper_soup = BeautifulSoup(requests.get(url=link).text,"lxml")
                pages = [f'https://www.gastearsivi.com{link["href"]}' for link in paper_soup.find_all("a",href=True,class_="StyledComponents__StyledLink-sc-1vz7aia-18 hBkgwa mr-1")]

                #downloading the pages
                for page in pages:

                    photo_soup = BeautifulSoup(requests.get(url=page).text,"lxml")
                    photo = photo_soup.find("img",src=True)["src"]
                    filename = photo.split("/")[-1]

                    if filename not in os.listdir(f"{name}/{newspaper_date}"):
                        response = requests.get(url=photo)

                        if response.status_code == 200:
                            with open(f"{name}/{newspaper_date}/{filename}","wb") as f:
                                f.write(response.content)
                            with open("download_results.txt","a") as f:
                                f.write(f"{name}/{newspaper_date}/{filename} was downloaded\n")
                            print(f"{name}/{newspaper_date}/{filename} was downloaded")
                        else:
                            with open("download_results.txt","a") as f:
                                f.write(f"{name}/{newspaper_date}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{name}/{newspaper_date}/{filename} was downloaded,it had response status code {response.status_code}")

    # The following method will check the entire archive
    def check_all(self):
        for i in range(len(self.newspapers)):
            self.check_newspaper(index=i)


if __name__ == "__main__":
    ga = GasteArsivi()


