# Al Ayam, Bahrain Newspaper
import time

import requests,os,lxml
import undetected_chromedriver as uc

from bs4 import BeautifulSoup

class AlAyamBahrain:
    def __init__(self):
        self.first_page = 1
        self.start_webdriver1()
        # self.start_webdriver2()
        self.page_count = self.return_pagecount()

    # The following method will start the selenium webdriver
    def start_webdriver1(self):
        chrome_options = uc.ChromeOptions()
        self.driver1 = uc.Chrome(options=chrome_options)



    # The following method will gather the page count
    def return_pagecount(self):
        website = f"https://www.alayam.com/archive/pdf?page=1"
        self.driver1.get(website)
        soup = BeautifulSoup(self.driver1.page_source,'lxml')
        pages = [int(page['href'].split("=")[-1]) for page in soup.find_all('a',href=True) if "page=" in page['href']]
        return max(pages)

    # The following method will download a particular page number
    def download_page(self,number:int):
        if self.first_page <= number <= self.page_count:
            website = f"https://www.alayam.com/archive/pdf?page={number}"
            self.driver1.get(website)
            soup = BeautifulSoup(self.driver1.page_source,'lxml')
            issues = []
            for issue in soup.find_all('a',href=True):
                if '#archive' in issue['href']:
                    if 'https://www.alayam.com' + issue['href'] not in issues:
                        issues.append('https://www.alayam.com' + issue['href'])
            for issue in issues:
                filename = issue.replace("#archive",'').split("/")
                d = filename[-1]
                m = filename[-2]
                y = filename[-3]
                filename = f"{d}-{m}-{y}.pdf"
                print(issue)
                self.driver1.get(issue)
                loop = True
                while True:
                    soup = BeautifulSoup(self.driver1.page_source, 'lxml')
                    pdf = soup.find(id='aPDFdownloadAllPages')
                    if pdf is None:
                        print(f"not found yet")
                        time.sleep(3)
                    else:
                        break
                response = requests.get(pdf['href'])
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open(f"download_results.txt",'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open(f"download_results.txt",'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one page to another later page
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.download_page(n1)
            n1 += 1

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(1,self.page_count)

    # The following method will check one page
    def check_page(self,number:int):
        if self.first_page <= number <= self.page_count:
            website = f"https://www.alayam.com/archive/pdf?page={number}"
            self.driver1.get(website)
            soup = BeautifulSoup(self.driver1.page_source,'lxml')
            issues = []
            for issue in soup.find_all('a',href=True):
                if '#archive' in issue['href']:
                    if 'https://www.alayam.com' + issue['href'] not in issues:
                        issues.append('https://www.alayam.com' + issue['href'])
            for issue in issues:
                filename = issue.replace("#archive",'').split("/")
                d = filename[-1]
                m = filename[-2]
                y = filename[-3]
                filename = f"{d}-{m}-{y}.pdf"
                if filename not in os.listdir():
                    print(issue)
                    self.driver1.get(issue)
                    loop = True
                    while True:
                        soup = BeautifulSoup(self.driver1.page_source, 'lxml')
                        pdf = soup.find(id='aPDFdownloadAllPages')
                        if pdf is None:
                            print(f"not found yet")
                            time.sleep(3)
                        else:
                            break
                    response = requests.get(pdf['href'])
                    if response.status_code == 200:
                        with open(f"{filename}",'wb') as f:
                            f.write(response.content)
                        with open(f"download_results.txt",'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open(f"download_results.txt",'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{filename} was already downloaded.")

    # The following method will download from one page to another later page
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.check_page(n1)
            n1 += 1

    # The following method will download the entire archive
    def check_all(self):
        self.check_n1_n2(1,self.page_count)

if __name__ == "__main__":
    aab = AlAyamBahrain()
    aab.check_n1_n2(1,2)