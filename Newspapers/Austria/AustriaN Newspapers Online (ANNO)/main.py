# ANNO Historische Zeitungen und Zeitschriften

import requests,os,lxml
from bs4 import BeautifulSoup

class Anno:
    def __init__(self):
        self.site = 'https://anno.onb.ac.at/alph_list.htm'
        self.newspaper_dictionary = {}
        self.gather_newspapers()

    # The following method will gather all the newspapers
    def gather_newspapers(self):
        soup = BeautifulSoup(requests.get(self.site).text,'lxml')
        for link in soup.select('h4 a')[::-1]:
            url = link['href']
            code = url.split("=")[-1]
            name = link.text
            key = f"{name}-{code}"
            value = url
            self.newspaper_dictionary[key] = value

    # The following method will print all the newspapers that start with a specific character
    def print_letter(self,char:str):
        for newspaper in self.newspaper_dictionary:
            if newspaper[0].lower() == char:
                print(newspaper)

    # This method will print the names of all the newspapers
    def print_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            print(newspaper)

    # The following method will download a specific newspaper on the archive
    def download_newspaper(self,newspaper:str)->None:
        if newspaper in self.newspaper_dictionary:
            os.mkdir(newspaper)
            code = self.newspaper_dictionary[newspaper].split("=")[-1]
            site = self.newspaper_dictionary[newspaper]
            soup1 = BeautifulSoup(requests.get(site).text,'lxml')
            years = []
            days_exist = True
            for link in soup1.find_all('a',href=True):
                if 'datum' in link['href']:
                    if "cgi-content" in link['href']:
                        years.append(f"https://anno.onb.ac.at{link['href'].replace('&zoom=33','')}")
                    elif "anno-plus" in link['href']:
                        days_exist = False
                        item = link['href'].replace("./","")
                        years.append(f"https://anno.onb.ac.at/cgi-content/{item}")
            print(years)
            for year in years:
                year_filename = year.split("=")[-1]
                os.mkdir(f"{newspaper}/{year_filename}")
                soup2 = BeautifulSoup(requests.get(url=year).text,'lxml')
                if days_exist:
                    days = [f"https://anno.onb.ac.at{link['href'].replace('&zoom=33','')}" for link in soup2.find_all('a',href=True) if 'datum=' in link['href']]
                    for day in days:
                        formatted_date = day.split("=")[-1]
                        os.mkdir(f"{newspaper}/{year_filename}/{formatted_date}")
                        number = 1
                        while True:
                            link = f'https://digital.onb.ac.at/rep/access/ANNO_{code}{formatted_date}/image/{number}'
                            response = requests.get(url=link)
                            if response.status_code == 200:
                                with open(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg",'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt','a') as f:
                                    f.write(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg was downloaded.\n")
                                print(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg was downloaded")
                                number += 1
                            elif 'File not found:' in response.text:
                                print(f'Last image was found')
                                break
                else:
                    numbers = []
                    h2s = soup2.find_all('h2')[1:]
                    for number in soup2.find_all('a',href=True,title=True):
                        if number['title'] == "Zum Dokument":
                            item = number['href'].replace("./", "")
                            link = f"https://anno.onb.ac.at/cgi-content/{item}"
                            file_name = h2s[len(numbers)].text
                            data_tuple = link,file_name
                            numbers.append(data_tuple)
                    for number in numbers:
                        filename = number[1]
                        filename = filename.replace("/","-")
                        try:
                            os.mkdir(f"{newspaper}/{year_filename}/{filename}")
                        except FileExistsError:
                            soup3 = BeautifulSoup(requests.get(url=number[0]).text,'lxml')
                        else:
                            images = []
                            for image in soup3.find_all('img'):
                                image_link = image['src'].split("?")[0]
                                if "https" in image['src']:
                                    images.append(image_link)
                            for i in range(len(images)):
                                response = requests.get(images[i])
                                if response.status_code == 200:
                                    with open(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg",'wb') as f:
                                        f.write(response.content)
                                    with open('download_results.txt','a') as f:
                                        f.write(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg was downloaded\n")
                                    print(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg was downloaded")

    # The following method will download all the newspapers on the archive
    def download_newspapers(self)->None:
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    # The following method will check if all the images for a specific newspaper were downloaded or not
    def check_newspaper(self,newspaper:str)->None:
        if newspaper in self.newspaper_dictionary:
            if not os.path.exists(newspaper):
                self.download_newspaper(newspaper)
            else:
                code = self.newspaper_dictionary[newspaper].split("=")[-1]
                site = self.newspaper_dictionary[newspaper]
                soup1 = BeautifulSoup(requests.get(site).text,'lxml')
                years = []
                days_exist = True
                for link in soup1.find_all('a',href=True):
                    if 'datum' in link['href']:
                        if "cgi-content" in link['href']:
                            years.append(f"https://anno.onb.ac.at{link['href'].replace('&zoom=33','')}")
                        elif "anno-plus" in link['href']:
                            days_exist = False
                            item = link['href'].replace("./","")
                            years.append(f"https://anno.onb.ac.at/cgi-content/{item}")
                print(years)
                for year in years:
                    year_filename = year.split("=")[-1]
                    try:
                        os.mkdir(f"{newspaper}/{year_filename}")
                    except FileExistsError:
                        pass
                    soup2 = BeautifulSoup(requests.get(url=year).text,'lxml')
                    if days_exist:
                        days = [f"https://anno.onb.ac.at{link['href'].replace('&zoom=33','')}" for link in soup2.find_all('a',href=True) if 'datum=' in link['href']]
                        for day in days:
                            formatted_date = day.split("=")[-1]
                            try:
                                os.mkdir(f"{newspaper}/{year_filename}/{formatted_date}")
                            except FileExistsError:
                                pass
                            number = 1
                            while True:
                                if f"{number}.jpeg" not in os.listdir(f"{newspaper}/{year_filename}/{formatted_date}"):
                                    link = f'https://digital.onb.ac.at/rep/access/ANNO_{code}{formatted_date}/image/{number}'
                                    response = requests.get(url=link)
                                    if response.status_code == 200:
                                        with open(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg",'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg was downloaded.\n")
                                        print(f"{newspaper}/{year_filename}/{formatted_date}/{number}.jpeg was downloaded")
                                        number += 1
                                    elif 'File not found:' in response.text:
                                        print(f'Last image was found')
                                        break
                                else:
                                    number += 1
                    else:
                        numbers = []
                        h2s = soup2.find_all('h2')[1:]
                        for number in soup2.find_all('a',href=True,title=True):
                            if number['title'] == "Zum Dokument":
                                item = number['href'].replace("./", "")
                                link = f"https://anno.onb.ac.at/cgi-content/{item}"
                                file_name = h2s[len(numbers)].text
                                data_tuple = link,file_name
                                numbers.append(data_tuple)
                        for number in numbers:
                            filename = number[1]
                            filename = filename.replace("/","-")
                            try:
                                os.mkdir(f"{newspaper}/{year_filename}/{filename}")
                            except FileExistsError:
                                pass
                            soup3 = BeautifulSoup(requests.get(url=number[0]).text,'lxml')
                            images = []
                            for image in soup3.find_all('img'):
                                image_link = image['src'].split("?")[0]
                                if "https" in image['src']:
                                    images.append(image_link)
                            for i in range(len(images)):
                                if f"{i+1}.jpeg" not in os.listdir(f"{newspaper}/{year_filename}/{filename}"):
                                    response = requests.get(images[i])
                                    if response.status_code == 200:
                                        with open(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg",'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg was downloaded.\n")
                                        print(f"{newspaper}/{year_filename}/{filename}/{i+1}.jpeg was downloaded")

    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

if __name__ == '__main__':
    anno = Anno()
    anno.check_newspaper(newspaper='Der Zweigverein Olmütz des patriotischen Landes- und Frauenhilfsvereines vom Roten Kreuze für Mähren. Tätigkeitsbericht (Thätigkeitsbericht)-rko')
