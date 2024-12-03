# Bermuda National Library archive
import requests,lxml,os,time,datetime
from selenium import webdriver
from bs4 import BeautifulSoup

class BermudaNationLibrary:
    def __init__(self):
        self.start_driver()
        self.newspaper_dictionary = {}
        self.get_newspapers()
        self.first_date = datetime.datetime(day=2,month=1,year=1900)

    # The following method will start the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method will the names of all the newspapers
    def get_newspapers(self)->None:
        self.driver.get('https://bnl.contentdm.oclc.org')
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        newspaper_titles = [h2.text for h2 in soup.find_all("h2")]
        newspaper_titles.pop(0)
        links = [f"https://bnl.contentdm.oclc.org{link['href']}/search" for link in soup.find_all("a",href=True) if  "/digital/collection/" in link['href']]
        for i in range(len(links)):
            self.newspaper_dictionary[newspaper_titles[i]] = links[i]

    # The following method will download all the names of the newspapers
    def print_newspaper_names(self)->None:
        for name in self.newspaper_dictionary:
            print(name)

    # The following method will how many pages there are for each newspaper
    def find_page_count(self,number:int)->int:
        if number < 20:
            return 1
        elif number % 20 == 0:
            return number//20
        else:
            return (number//20)+1

    # The following method will download a newspaper that is on the website
    def download_newspaper(self,newspaper:str):
        if newspaper == 'Royal Gazette (1784 - 1964)':
            self.download_royal_gazette()
        elif newspaper in self.newspaper_dictionary:
            page = self.newspaper_dictionary[newspaper]
            self.driver.get(page)
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            h3 = [h3.text.replace(",",'') for h3 in soup.find_all("h3") if "Records 1-" in h3.text]
            number = int(h3[0].split()[-1])
            page_count = self.find_page_count(number)

            for i in range(1,page_count+1):
                site = f"{page}/page/{i}"
                print(site)
                self.driver.get(site)
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source,'lxml')

                links = [f'https://bnl.contentdm.oclc.org{image['src']}' for image in soup.find_all("img",src=True) if "api" in image['src']]
                links = [link for link in links if requests.get(link).status_code == 200]
                divs = [div.text for div in soup.find_all('div', class_="MetadataField-content truncation")]
                print(links)

                # gets the dates of the newspapers
                dates = []
                for i in range(len(divs)):
                    div = divs[i]
                    if div == "PDF" or div == 'Microfilm' or div in self.newspaper_dictionary:
                        continue
                    elif "January" in div or "February" in div or "March" in div or "April" in div or "May" in div or "June" in div or "July" in div or "August" in div or "September" in div or "October" in div or "November" in div or "December" in div:
                        dates.append(div)
                    elif "-" in div:
                        dates.append(div)
                    elif len(div) == 4:
                        numbers = ['0','1','2','3','4','5','6','7','8','9']
                        total = sum([1 for char in div if char in numbers])
                        if total == 4:
                            dates.append(div)

                try:
                    os.mkdir(newspaper)
                except FileExistsError:
                    pass

                for i in range(len(links)):
                    link = links[i]
                    response = requests.get(url=link)
                    split_form = link.split("/")
                    collection_type = split_form[-4]
                    id_type = split_form[-2]

                    string = "https://bnl.contentdm.oclc.org/digital/api/collection/p16347coll6/id/237/page/0/inline/p16347coll6_237_0"
                    pdf_file = f"https://bnl.contentdm.oclc.org/digital/api/collection/{collection_type}/id/{id_type}/page/0/inline/{collection_type}_{id_type}_0"

                    filename = f"{newspaper} {dates[i]} {id_type}.pdf"

                    response = requests.get(url=pdf_file)

                    if response.status_code == 200:
                        with open(f"{newspaper}/{filename}",'wb') as f:
                            f.write(response.content)
                        with open("download_results.txt","a") as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open("download_results.txt","a") as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    def check_newspaper(self,newspaper:str):
        if newspaper == 'Royal Gazette (1784 - 1964)':
            self.check_royal_gazette()
        elif newspaper in self.newspaper_dictionary:
            try:
                items = os.listdir(newspaper)
            except FileNotFoundError:
                pass
            else:
                page = self.newspaper_dictionary[newspaper]
                self.driver.get(page)
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                h3 = [h3.text.replace(",", '') for h3 in soup.find_all("h3") if "Records 1-" in h3.text]

                if h3:
                    number = int(h3[0].split()[-1])
                else:
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    h3 = [h3.text.replace(",", '') for h3 in soup.find_all("h3") if "Records 1-" in h3.text]
                    number = int(h3[0].split()[-1])
                page_count = self.find_page_count(number)

                for i in range(1, page_count + 1):
                    site = f"{page}/page/{i}"
                    print(site)
                    self.driver.get(site)
                    time.sleep(2)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')

                    links = [f'https://bnl.contentdm.oclc.org{image['src']}' for image in soup.find_all("img", src=True) if
                             "api" in image['src']]
                    links = [link for link in links if requests.get(link).status_code == 200]
                    divs = [div.text for div in soup.find_all('div', class_="MetadataField-content truncation")]
                    print(links)

                    # gets the dates of the newspapers
                    dates = []
                    for i in range(len(divs)):
                        div = divs[i]
                        if div == "PDF" or div == 'Microfilm' or div in self.newspaper_dictionary:
                            continue
                        elif "January" in div or "February" in div or "March" in div or "April" in div or "May" in div or "June" in div or "July" in div or "August" in div or "September" in div or "October" in div or "November" in div or "December" in div:
                            dates.append(div)
                        elif "-" in div:
                            dates.append(div)
                        elif len(div) == 4:
                            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                            total = sum([1 for char in div if char in numbers])
                            if total == 4:
                                dates.append(div)

                    try:
                        os.mkdir(newspaper)
                    except FileExistsError:
                        pass

                    for i in range(len(links)):
                        link = links[i]
                        response = requests.get(url=link)
                        split_form = link.split("/")
                        collection_type = split_form[-4]
                        id_type = split_form[-2]

                        #string = "https://bnl.contentdm.oclc.org/digital/api/collection/p16347coll6/id/237/page/0/inline/p16347coll6_237_0"
                        pdf_file = f"https://bnl.contentdm.oclc.org/digital/api/collection/{collection_type}/id/{id_type}/page/0/inline/{collection_type}_{id_type}_0"

                        filename = f"{newspaper} {dates[i]} {id_type}.pdf"

                        if filename not in items:

                            response = requests.get(url=pdf_file)

                            if response.status_code == 200:
                                with open(f"{newspaper}/{filename}", 'wb') as f:
                                    f.write(response.content)
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{filename} was downloaded.\n")
                                print(f"{filename} was downloaded.")
                            else:
                                with open("download_results.txt", "a") as f:
                                    f.write(
                                        f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

    # A specific method had to be coded to download one of the methods
    def download_royal_gazette(self):
        newspaper = 'Royal Gazette (1784 - 1964)'
        page = 'https://bnl.contentdm.oclc.org/digital/collection/BermudaNP02/search'
        self.driver.get(page)
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        h3 = [h3.text.replace(",", '') for h3 in soup.find_all("h3") if "Records 1-" in h3.text]
        number = int(h3[0].split()[-1])
        page_count = self.find_page_count(number)
        for i in range(1, page_count + 1):
            site = f"{page}/page/{i}"
            self.driver.get(site)
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            links = [f'https://bnl.contentdm.oclc.org{link['href']}' for link in soup.find_all("a", href=True) if "digital/collection" in link['href'] and '/rec/' in link['href']]
            print(links)
            links = [link for link in links if requests.get(link).status_code == 200]
            divs = [div.text for div in soup.find_all('div', class_="MetadataField-content truncation")]

            # gets the dates of the newspapers
            dates = []
            for i in range(len(divs)):
                div = divs[i]
                if div == "PDF" or div == 'Microfilm' or div in self.newspaper_dictionary:
                    continue
                elif "January" in div or "February" in div or "March" in div or "April" in div or "May" in div or "June" in div or "July" in div or "August" in div or "September" in div or "October" in div or "November" in div or "December" in div:
                    dates.append(div)
                elif "-" in div:
                    dates.append(div)
                elif len(div) == 4:
                    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    total = sum([1 for char in div if char in numbers])
                    if total == 4:
                        dates.append(div)

            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass

            for i in range(len(links)):
                date = dates[i]
                datetime_format = date.split('-')
                datetime_format = datetime.datetime(day=int(datetime_format[-1]),month=int(datetime_format[1]),year=int(datetime_format[0]))

                if datetime_format >= self.first_date:
                    print('hi')
                    'https://bnl.contentdm.oclc.org/digital/collection/BermudaNP02/id/30273/rec/5899#'
                    'https://bnl.contentdm.oclc.org/digital/api/collection/BermudaNP02/id/30273/page/0/inline/BermudaNP02_30273_0'
                    link = links[i]
                    response = requests.get(url=link)
                    split_form = link.split("/")
                    collection_type = split_form[-4]
                    id_type = split_form[-2]

                    pdf_file = f"https://bnl.contentdm.oclc.org/digital/api/collection/{collection_type}/id/{id_type}/page/0/inline/{collection_type}_{id_type}_0"

                    number = link.split('/')[-3]
                    filename = f"{newspaper} {dates[i]} {number}.pdf"
                    pdf_file = f'https://bnl.contentdm.oclc.org/digital/api/collection/BermudaNP02/id/{number}/page/0/inline/BermudaNP02_{number}_0'
                    response = requests.get(url=pdf_file)
                    if response.status_code == 200:
                        with open(f"{newspaper}/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")

                else:
                    try:
                        os.mkdir(f"{newspaper}/{date}")
                    except FileExistsError:
                        pass
                    link = links[i]
                    self.driver.get(link)
                    time.sleep(1)
                    soup = BeautifulSoup(self.driver.page_source,'lxml')
                    images = [int(image['src'].split("/")[-2]) for image in soup.find_all('img',src=True) if 'api' in image['src']]
                    numbers =[]
                    for n in images:
                        if n not in numbers:
                            numbers.append(n)

                    for n in numbers:
                        new_link = f"https://bnl.contentdm.oclc.org/digital/download/collection/BermudaNP02/id/{n}/size/full"
                        response = requests.get(new_link)
                        if response.status_code == 200:
                            with open(f'{newspaper}/{date}/{n}.jpg','wb') as f:
                                f.write(response.content)
                            with open('download_results.txt','a') as f:
                                f.write(f'{newspaper}/{date}/{n}.jpg was downloaded.\n')
                            print(f'{newspaper}/{date}/{n}.jpg was downloaded.')
                        else:
                            with open('download_results.txt','a') as f:
                                f.write(f'{newspaper}/{date}/{n}.jpg was not downloaded,it had response status code {response.status_code}\n')
                            print(f'{newspaper}/{date}/{n}.jpg was downloaded,it had response status code {response.status_code}')


    # A specific method had to be coded to check one of the newspapers
    def check_royal_gazette(self):
        page = 'https://bnl.contentdm.oclc.org/digital/collection/BermudaNP02/search'
        try:
            days = os.listdir('Royal Gazette (1784 - 1964)')
        except FileNotFoundError:
            self.download_royal_gazette()
        else:
            newspaper = 'Royal Gazette (1784 - 1964)'
            page = 'https://bnl.contentdm.oclc.org/digital/collection/BermudaNP02/search'
            self.driver.get(page)
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            h3 = [h3.text.replace(",", '') for h3 in soup.find_all("h3") if "Records 1-" in h3.text]
            number = int(h3[0].split()[-1])
            page_count = self.find_page_count(number)
            for i in range(1, page_count + 1):
                site = f"{page}/page/{i}"
                self.driver.get(site)
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')

                links = [f'https://bnl.contentdm.oclc.org{link['href']}' for link in soup.find_all("a", href=True) if "digital/collection" in link['href'] and '/rec/' in link['href']]
                print(links)
                links = [link for link in links if requests.get(link).status_code == 200]
                divs = [div.text for div in soup.find_all('div', class_="MetadataField-content truncation")]

                # gets the dates of the newspapers
                dates = []
                for i in range(len(divs)):
                    div = divs[i]
                    if div == "PDF" or div == 'Microfilm' or div in self.newspaper_dictionary:
                        continue
                    elif "January" in div or "February" in div or "March" in div or "April" in div or "May" in div or "June" in div or "July" in div or "August" in div or "September" in div or "October" in div or "November" in div or "December" in div:
                        dates.append(div)
                    elif "-" in div:
                        dates.append(div)
                    elif len(div) == 4:
                        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        total = sum([1 for char in div if char in numbers])
                        if total == 4:
                            dates.append(div)

                try:
                    os.mkdir(newspaper)
                except FileExistsError:
                    pass

                for i in range(len(links)):
                    date = dates[i]
                    datetime_format = date.split('-')
                    datetime_format = datetime.datetime(day=int(datetime_format[-1]), month=int(datetime_format[1]),year=int(datetime_format[0]))
                    print(datetime_format,self.first_date,datetime_format >= self.first_date)
                    if datetime_format >= self.first_date:
                        print('hi')
                        'https://bnl.contentdm.oclc.org/digital/collection/BermudaNP02/id/30273/rec/5899#'
                        'https://bnl.contentdm.oclc.org/digital/api/collection/BermudaNP02/id/30273/page/0/inline/BermudaNP02_30273_0'
                        link = links[i]
                        response = requests.get(url=link)
                        split_form = link.split("/")
                        collection_type = split_form[-4]
                        id_type = split_form[-2]

                        pdf_file = f"https://bnl.contentdm.oclc.org/digital/api/collection/{collection_type}/id/{id_type}/page/0/inline/{collection_type}_{id_type}_0"

                        number = link.split('/')[-3]
                        filename = f"{newspaper} {dates[i]} {number}.pdf"
                        pdf_file = f'https://bnl.contentdm.oclc.org/digital/api/collection/BermudaNP02/id/{number}/page/0/inline/BermudaNP02_{number}_0'
                        if filename not in os.listdir('Royal Gazette (1784 - 1964)'):
                            response = requests.get(url=pdf_file)
                            if response.status_code == 200:
                                with open(f"{newspaper}/{filename}", 'wb') as f:
                                    f.write(response.content)
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{filename} was downloaded.\n")
                                print(f"{filename} was downloaded.")
                            else:
                                with open("download_results.txt", "a") as f:
                                    f.write(
                                        f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{filename} was not downloaded,it had response status code {response.status_code}")
                    else:
                        try:
                            os.mkdir(f"{newspaper}/{date}")
                        except FileExistsError:
                            pass
                        link = links[i]
                        self.driver.get(link)
                        time.sleep(1)
                        soup = BeautifulSoup(self.driver.page_source, 'lxml')
                        images = [int(image['src'].split("/")[-2]) for image in soup.find_all('img', src=True) if'api' in image['src']]
                        numbers = []
                        for n in images:
                            if n not in numbers:
                                numbers.append(n)

                        for n in numbers:
                            if f'{n}.jpg' not in os.listdir(f"{newspaper}/{date}"):
                                new_link = f"https://bnl.contentdm.oclc.org/digital/download/collection/BermudaNP02/id/{n}/size/full"
                                response = requests.get(new_link)
                                if response.status_code == 200:
                                    with open(f'{newspaper}/{date}/{n}.jpg', 'wb') as f:
                                        f.write(response.content)
                                    with open('download_results.txt', 'a') as f:
                                        f.write(f'{newspaper}/{date}/{n}.jpg was downloaded.\n')
                                    print(f'{newspaper}/{date}/{n}.jpg was downloaded.')
                                else:
                                    with open('download_results.txt', 'a') as f:
                                        f.write(f'{newspaper}/{date}/{n}.jpg was not downloaded,it had response status code {response.status_code}\n')
                                    print(f'{newspaper}/{date}/{n}.jpg was downloaded,it had response status code {response.status_code}')

if __name__ == "__main__":
    bnl = BermudaNationLibrary()
    bnl.check_royal_gazette()
