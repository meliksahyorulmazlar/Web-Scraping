# Pyongyang Times Webscraper

import requests,lxml,os
from bs4 import BeautifulSoup


class PyongyangTimes:
    def __init__(self):
        self.main_page = 'http://www.pyongyangtimes.com.kp/pdf'

    # This method will download all the pdfs
    def download_pdfs(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text,'lxml')
        pages = [link.text for link in soup.select('li',class_='rc-pagination-item rc-pagination-item-2',title=True,tabindex=True)]
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        page_count = 1
        for page in pages:
            if page:
                count = 0
                for char in page:
                    if char in numbers:
                        count += 1
                if count == len(page):
                    if int(page) > page_count:
                        page_count = int(page)

        for i in range(1,page_count+1):
            site = f"http://www.pyongyangtimes.com.kp/pdf?num={i}"
            soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            pdfs = [f"http://www.pyongyangtimes.com.kp{pdf['href']}" for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            numbers = [number.text for number in soup.find_all('p',class_='no')]
            dates = [date.text for date in soup.find_all('p', class_='date')]

            for i in range(len(pdfs)):
                pdf = pdfs[i]
                number = numbers[i]
                date = dates[i]
                filename = f"{number} {date}.pdf"
                response = requests.get(url=pdf)
                if response.status_code == 200:
                    with open(f"{filename}","wb") as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded,it had response status code {response.status_code}")

    # This method checks if there are any missing pdfs to be downloaded etc
    def check_pdfs(self):
        soup = BeautifulSoup(requests.get(url=self.main_page).text, 'lxml')
        pages = [link.text for link in soup.select('li', class_='rc-pagination-item rc-pagination-item-2', title=True, tabindex=True)]
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        page_count = 1
        for page in pages:
            if page:
                count = 0
                for char in page:
                    if char in numbers:
                        count += 1
                if count == len(page):
                    if int(page) > page_count:
                        page_count = int(page)

        for i in range(1, page_count + 1):
            site = f"http://www.pyongyangtimes.com.kp/pdf?num={i}"
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = [f"http://www.pyongyangtimes.com.kp{pdf['href']}" for pdf in soup.find_all('a', href=True) if
                    '.pdf' in pdf['href']]
            numbers = [number.text for number in soup.find_all('p', class_='no')]
            dates = [date.text for date in soup.find_all('p', class_='date')]

            for i in range(len(pdfs)):
                pdf = pdfs[i]
                number = numbers[i]
                date = dates[i]
                filename = f"{number} {date}.pdf"
                if filename not in os.listdir():
                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f"{filename}", "wb") as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded,it had response status code {response.status_code}")

if __name__ == "__main__":
    pt = PyongyangTimes()
    pt.download_pdfs()