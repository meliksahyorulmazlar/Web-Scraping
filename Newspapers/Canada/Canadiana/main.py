# Canadiana archive
# Monographs
# Government Publications
# Annuals
# Periodicals
# Newspapers


import requests,os,lxml,json
from bs4 import BeautifulSoup

#85986 monographs
#8232 government publications
#2682 annuals
#1998 periodicals
#647 newspapers

class Canadiana:
    def __init__(self):
        self.monograph_site = "https://www.canadiana.ca/search/browsable/1?collection=monog"
        self.government_publications_site = "https://www.canadiana.ca/search/browsable/1?collection=govpubs"
        self.annuals_site = "https://www.canadiana.ca/search/browsable/1?collection=annuals"
        self.periodicals_site = "https://www.canadiana.ca/search/browsable/1?collection=per"
        self.newspapers_site = "https://www.canadiana.ca/search/browsable/1?collection=news"
        self.categories = {"newspapers":"https://www.canadiana.ca/search/browsable/1?collection=news",'periodicals':"https://www.canadiana.ca/search/browsable/1?collection=per",'annuals':"https://www.canadiana.ca/search/browsable/1?collection=annuals",'government':"https://www.canadiana.ca/search/browsable/1?collection=govpubs",'monographs':"https://www.canadiana.ca/search/browsable/1?collection=monog"}
        # self.monograph_count = 0
        # self.government_publications_count = 0
        # self.annuals_count = 0
        # self.periodicals_count = 0
        # self.newspapers_count = 0

    # The following method will print the names of all the categories
    def print_category_names(self)->None:
        for key, value in self.categories.items():
            count = self.find_page_count(value)
            print(f"category:\n{key}\nwebsite:{key}\npage count {count}")


    # The following method will find the page count for any page given to it
    def find_page_count(self,page)->int:
        soup = BeautifulSoup(requests.get(url=page).text,'lxml')
        pages = [int(page.text) for page in soup.find_all("a",href=True,class_='page-link') if page.text != "Next"]
        return max(pages)

    # The following method will download a particular given category if it exists
    def download_category(self,category)->None:
        if category in self.categories:
            os.mkdir(category)
            website = f"{self.categories[category]}"
            pages = self.find_page_count(website)
            for page in range(1,pages+1):
                new_website = f"{website}".replace("1",str(page))
                soup = BeautifulSoup(requests.get(new_website).text,'lxml')
                names = {}
                for name in soup.find_all('a',href=True):
                    if 'oocihm' in name['href'] and name["href"]!= name.text.strip():
                        value = name['href']
                        code = value.split("/")[-1]
                        key = name.text.strip().replace("/","").replace(":","") + f"-{code}"
                        names[key] = value
                        os.mkdir(f"{category}/{key}")
                        new_soup = BeautifulSoup(requests.get(value).text,'lxml')
                        image_link = new_soup.find(id='pvFullImageDownload')
                        if image_link is None:
                            issues = [(issue.text.replace("/","_").replace(":",""),issue['href']) for issue in new_soup.find_all(class_='stretched-link')]
                            for issue in issues:
                                code = issue[1].split("/")[-1]
                                directory = f"{issue[0]}-{code}".replace("/","_").replace(":","")
                                new_soup = BeautifulSoup(requests.get(issue[1]).text,'lxml')
                                try:
                                    pdf_link = new_soup.find(id='pvDownloadFull')['href']
                                except KeyError:
                                    os.mkdir(f"{category}/{key}/{directory}")
                                    number = 1
                                    while True:
                                        website = f'{issue[1]}/{number}'
                                        image_soup = BeautifulSoup(requests.get(website).text,'lxml')
                                        try:
                                            image_link = image_soup.find(id='pvFullImageDownload')['data-url']
                                        except TypeError:
                                            break
                                        response = requests.get(image_link)
                                        if response.status_code == 200:
                                            with open(f'{category}/{key}/{directory}/{number}.jpg','wb') as f:
                                                f.write(response.content)
                                            with open('download_results.txt','a') as f:
                                                f.write(f"{category}/{key}/{directory}/{number}.jpg was downloaded.\n")
                                            print(f"{category}/{key}/{directory}/{number}.jpg was downloaded.")
                                            number += 1
                                        else:
                                            with open('download_results.txt','a') as f:
                                                f.write(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.\n")
                                            print(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.")
                                else:
                                    filename = f"{directory}.pdf"
                                    response = requests.get(pdf_link)
                                    if response.status_code == 200:
                                        with open(f"{category}/{key}/{filename}",'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{category}/{key}/{filename} was downloaded.\n")
                                        print(f"{category}/{key}/{filename} was downloaded")
                                    else:
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                                        print(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}")
                        else:
                            try:
                                pdf_link = new_soup.find(id='pvDownloadFull')['href']
                                filename = f"{key}-{code}.pdf"
                            except KeyError:
                                directory = f"{key}-{code}"
                                number = 1
                                while True:
                                    website = f'{value}/{number}'
                                    image_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                                    try:
                                        image_link = image_soup.find(id='pvFullImageDownload')['data-url']
                                    except TypeError:
                                        break
                                    response = requests.get(image_link)
                                    if response.status_code == 200:
                                        with open(f'{category}/{key}/{directory}/{number}.jpg', 'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt', 'a') as f:
                                            f.write(f"{category}/{key}/{directory}/{number}.jpg was downloaded.\n")
                                        print(f"{category}/{key}/{directory}/{number}.jpg was downloaded.")
                                        number += 1
                                    else:
                                        with open('download_results.txt', 'a') as f:
                                            f.write(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.\n")
                                        print(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.")
                                    print(website)
                            else:
                                response = requests.get(pdf_link)
                                if response.status_code == 200:
                                    with open(f"{category}/{key}/{filename}",'wb') as f:
                                        f.write(response.content)
                                    with open('download_results.txt','a') as f:
                                        f.write(f"{category}/{key}/{filename} was downloaded.\n")
                                    print(f"{category}/{key}/{filename} was downloaded.")
                                else:
                                    with open('download_results.txt','a') as f:
                                        f.write(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}")
                                    print(f"{category}/{key}/{filename} was downloaded, it had response status code {response.status_code}")


    # The following method will download all the categories on the archive
    def download_categories(self)->None:
        for category in self.categories:
            self.download_category(category)

    # The following method will check a particular category
    def check_category(self,category:str)->None:
        if category in self.categories:
            try:
                os.mkdir(category)
            except FileExistsError:
                pass
            website = f"{self.categories[category]}"
            pages = self.find_page_count(website)
            for page in range(1,pages+1):
                new_website = f"{website}".replace("1",str(page))
                soup = BeautifulSoup(requests.get(new_website).text,'lxml')
                names = {}
                for name in soup.find_all('a',href=True):
                    if 'oocihm' in name['href'] and name["href"]!= name.text.strip():
                        value = name['href']
                        code = value.split("/")[-1]
                        key = name.text.strip().replace("/","").replace(":","") + f"-{code}"
                        names[key] = value
                        try:
                            os.mkdir(f"{category}/{key}")
                        except FileExistsError:
                            pass
                        new_soup = BeautifulSoup(requests.get(value).text,'lxml')
                        image_link = new_soup.find(id='pvFullImageDownload')
                        if image_link is None:
                            issues = [(issue.text.replace("/","_").replace(":",""),issue['href']) for issue in new_soup.find_all(class_='stretched-link')]
                            for issue in issues:
                                code = issue[1].split("/")[-1]
                                directory = f"{issue[0]}-{code}".replace("/","_").replace(":","")
                                new_soup = BeautifulSoup(requests.get(issue[1]).text,'lxml')
                                try:
                                    pdf_link = new_soup.find(id='pvDownloadFull')['href']
                                except KeyError:
                                    try:
                                        os.mkdir(f"{category}/{key}/{directory}")
                                    except FileExistsError:
                                        pass
                                    number = 1
                                    while True:
                                        if f"{number}.jpg" not in os.listdir(f"{category}/{key}/{directory}"):
                                            website = f'{issue[1]}/{number}'
                                            image_soup = BeautifulSoup(requests.get(website).text,'lxml')
                                            try:
                                                image_link = image_soup.find(id='pvFullImageDownload')['data-url']
                                            except TypeError:
                                                break
                                            response = requests.get(image_link)
                                            if response.status_code == 200:
                                                with open(f'{category}/{key}/{directory}/{number}.jpg','wb') as f:
                                                    f.write(response.content)
                                                with open('download_results.txt','a') as f:
                                                    f.write(f"{category}/{key}/{directory}/{number}.jpg was downloaded.\n")
                                                print(f"{category}/{key}/{directory}/{number}.jpg was downloaded.")
                                                number += 1
                                            else:
                                                with open('download_results.txt','a') as f:
                                                    f.write(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.\n")
                                                print(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.")
                                            print(website)
                                        else:
                                            print(f"{category}/{key}/{directory}/{number}.jpg was already downloaded.")
                                            number += 1
                                else:
                                    filename = f"{directory}.pdf"
                                    response = requests.get(pdf_link)
                                    if filename not in os.listdir(f"{category}/{key}"):
                                        if response.status_code == 200:
                                            with open(f"{category}/{key}/{filename}",'wb') as f:
                                                f.write(response.content)
                                            with open('download_results.txt','a') as f:
                                                f.write(f"{category}/{key}/{filename} was downloaded.\n")
                                            print(f"{category}/{key}/{filename} was downloaded")
                                        else:
                                            with open('download_results.txt','a') as f:
                                                f.write(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}\n")
                                            print(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}")
                                    else:
                                        print(f"{category}/{key}/{filename} was already downloaded")
                        else:
                            try:
                                pdf_link = new_soup.find(id='pvDownloadFull')['href']
                                filename = f"{key}-{code}.pdf"
                            except KeyError:
                                directory = f"{key}-{code}"
                                number = 1
                                while True:
                                    if f"{number}.jpg" not in os.listdir(f"{category}/{key}/{directory}"):
                                        website = f'{value}/{number}'
                                        image_soup = BeautifulSoup(requests.get(website).text, 'lxml')
                                        try:
                                            image_link = image_soup.find(id='pvFullImageDownload')['data-url']
                                        except TypeError:
                                            break

                                        response = requests.get(image_link)
                                        if response.status_code == 200:
                                            with open(f'{category}/{key}/{directory}/{number}.jpg', 'wb') as f:
                                                f.write(response.content)
                                            with open('download_results.txt', 'a') as f:
                                                f.write(f"{category}/{key}/{directory}/{number}.jpg was downloaded.\n")
                                            print(f"{category}/{key}/{directory}/{number}.jpg was downloaded.")
                                            number += 1
                                        else:
                                            with open('download_results.txt', 'a') as f:
                                                f.write(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.\n")
                                            print(f"{category}/{key}/{directory}/{number}.jpg was not downloaded.")
                                    else:
                                        print(f"{category}/{key}/{directory}/{number}.jpg was already downloaded.")
                                        number += 1
                            else:
                                if filename not in os.listdir(f"{category}/{key}"):
                                    response = requests.get(pdf_link)
                                    if response.status_code == 200:
                                        with open(f"{category}/{key}/{filename}",'wb') as f:
                                            f.write(response.content)
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{category}/{key}/{filename} was downloaded.\n")
                                        print(f"{category}/{key}/{filename} was downloaded.")
                                    else:
                                        with open('download_results.txt','a') as f:
                                            f.write(f"{category}/{key}/{filename} was not downloaded, it had response status code {response.status_code}")
                                        print(f"{category}/{key}/{filename} was downloaded, it had response status code {response.status_code}")
                                else:
                                    print(f"{category}/{key}/{filename} was already downloaded.")

    # The following method will check all the categories on the archive
    def check_categories(self):
        for category in self.categories:
            self.check_category(category)

if __name__ == "__main__":
    canadiana = Canadiana()
    # canadiana.download_categories()
    canadiana.check_category('government')
