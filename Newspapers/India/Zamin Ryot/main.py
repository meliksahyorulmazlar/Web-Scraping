# Zamin Ryot Webscraper

import requests,os,lxml,datetime
from bs4 import BeautifulSoup

class ZaminRyot:
    def __init__(self):
        self.page = 'http://www.zaminryot.com/archives/index.html'
        soup = BeautifulSoup(requests.get(url=self.page).text,'lxml')
        self.links = [link['href'].replace("../","").replace('./','') for link in soup.select('li span a')]
        self.current_year = datetime.datetime.now().year


    # The following method will download a specific year between 1930 and the current year that we are in
    def download_year(self,year:int):
        links = []

        for link in self.links:
            if f"{year}/" in link:
               links.append(link)
        print(links)
        if links:
            os.mkdir(f"{year}")

            for link in links:
                if 'pdf' in link:
                    site = f"http://www.zaminryot.com/{link}"
                    filename = site.split("/")[-1]

                    response = requests.get(url=site)
                    if response.status_code == 200:
                        with open(f'{year}/{filename}','wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{year}/{filename} was downloaded.\n")
                        print(f"{year}/{filename} was downloaded.")
                else:
                    date = link.split("/")[-2]
                    os.mkdir(f"{year}/{date}")
                    site = link.replace('index.html',f'images/{date}-main1.jpg')
                    site = f'http://www.zaminryot.com/{site}'
                    for i in range(1,17):
                        new_site = site.replace("1.jpg", f"{i}.jpg")
                        print(new_site)
                        response = requests.get(url=new_site)
                        if response.status_code == 200:
                            with open(f"{year}/{date}/{i}.jpg",'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt','a') as f:
                                f.write(f'{year}/{date}/{i}.jpg was downloaded.\n')
                            print(f'{year}/{date}/{i}.jpg was downloaded.')
                        else:
                            with open('download_results.txt','a') as f:
                                f.write(f'{year}/{date}/{i}.jpg was not downloaded, it had response status code {response.status_code}\n')
                            print(f'{year}/{date}/{i}.jpg was not downloaded, it had response status code {response.status_code}')


    # The following method will download the entire archive
    def download_years(self):
        for year in range(1930,self.current_year+1):
            self.download_year(year)

    # The following year will check a specific year if all the newspapers have been downloaded for that specific year
    def check_year(self,year:int):
        links = []
        for link in self.links:
            if f"{year}/" in link:
                links.append(link)

        if links:
            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass

            for link in links:
                if 'pdf' in link:
                    site = f"http://www.zaminryot.com/{link}"
                    filename = site.split("/")[-1]
                    if filename not in os.listdir(f"{year}"):
                        response = requests.get(url=site)
                        if response.status_code == 200:
                            with open(f'{year}/{filename}', 'wb') as f:
                                f.write(response.content)
                            with open('download_results.txt', 'a') as f:
                                f.write(f"{year}/{filename} was downloaded.\n")
                            print(f"{year}/{filename} was downloaded.")
                else:
                    date = link.split("/")[-2]
                    try:
                        os.mkdir(f"{year}/{date}")
                    except FileExistsError:
                        pass

                    site = link.replace('index.html', f'images/{date}-main1.jpg')
                    site = f'http://www.zaminryot.com/{site}'
                    for i in range(1, 17):
                        new_site = site.replace("1.jpg", f"{i}.jpg")
                        print(new_site)
                        if f"{i}.jpg" not in os.listdir(f"{year}/{date}"):
                            response = requests.get(url=new_site)
                            if response.status_code == 200:
                                with open(f"{year}/{date}/{i}.jpg", 'wb') as f:
                                    f.write(response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f'{year}/{date}/{i}.jpg was downloaded.\n')
                                print(f'{year}/{date}/{i}.jpg was downloaded.')
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f'{year}/{date}/{i}.jpg was not downloaded, it had response status code {response.status_code}\n')
                                print(f'{year}/{date}/{i}.jpg was not downloaded, it had response status code {response.status_code}')

    # The following method will check the entire archive
    def check_years(self):
        for year in range(1930,self.current_year+1):
            self.check_year(year)


if __name__ == "__main__":
    zr = ZaminRyot()
    zr.check_year(year=2015)
