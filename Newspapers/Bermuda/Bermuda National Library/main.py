# Bermuda National Library archive
import requests,lxml,os,time
from selenium import webdriver
from bs4 import BeautifulSoup

class BermudaNationLibrary:
    def __init__(self):
        self.start_driver()
        self.newspaper_dictionary = {}
        self.get_newspapers()

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
        if newspaper in self.newspaper_dictionary:
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
        if newspaper in self.newspaper_dictionary:
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

    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)




if __name__ == "__main__":
    bnl = BermudaNationLibrary()
    bnl.check_newspaper(newspaper='Bermuda Beacon')
