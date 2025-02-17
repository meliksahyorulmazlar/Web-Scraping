# Akhbar Al Khaleej, newspaper from Bahrain
import os

import requests
from bs4 import BeautifulSoup


class AkhbarAlKhaleej:
    def __init__(self):
        self.start = 16411
        self.last = self.return_last_issue()


    # The following method will return the last issue
    def return_last_issue(self):
        website = f"https://akhbar-alkhaleej.com/#"
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [int(page['href'].split("=")[-1]) for page in soup.find_all('a',href=True) if 'pdf.php' in page['href']]
        return max(pages)

    # The following method will print the number of the last issue on the archive
    def print_last_page(self):
        print(self.last)

    # The following method will download the pdf of a particular number
    def download_issue(self,number:int):
        if self.start <= number <= self.last:
            website = f'https://media.akhbar-alkhaleej.com/source/{number}/pdf/1-Supplime/{number}.pdf'
            response = requests.get(website)
            if response.status_code == 200:
                with open(f"{number}.pdf",'wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{number}.pdf was downloaded.\n")
                print(f"{number}.pdf was downloaded.")
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{number}.pdf was not downloaded, it had response status code {response.status_code}\n")
                print(f"{number}.pdf was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one number to another later number
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.download_issue(i)

    # The following method will download the entire archive
    def download_all(self):
        self.download_n1_n2(self.start,self.last)

        # The following method will download the pdf of a particular number

    def check_issue(self, number: int):
        if self.start <= number <= self.last:
            if f"{number}.pdf" not in os.listdir():
                website = f'https://media.akhbar-alkhaleej.com/source/{number}/pdf/1-Supplime/{number}.pdf'
                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"{number}.pdf", 'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{number}.pdf was downloaded.\n")
                    print(f"{number}.pdf was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{number}.pdf was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{number}.pdf was not downloaded, it had response status code {response.status_code}")
            else:
                print(f"{number}.pdf was already downloaded")
                
    # The following method will check from one number to another later number
    def check_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1, n2 + 1):
            self.check_issue(i)

    # The following method will check the entire archive
    def check_all(self):
        self.check_n1_n2(self.start, self.last)

if __name__ == "__main__":
    akhbar_khaleej = AkhbarAlKhaleej()