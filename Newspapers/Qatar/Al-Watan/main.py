# Al-Watan, Qatari Newspaper

from bs4 import BeautifulSoup
import requests,lxml,os

class AlWatanQatar:
    def __init__(self):
        self.minimum = 1
        self.maximum = 0
        self.publications_count = 0
        self.find_page_count()


    # There are 2 categories : pdfs and publications

    # The following method will find how many pages each page has for publications and for pdfs
    def find_page_count(self):
        # Publications
        site = 'https://www.al-watan.com/اصدارات'
        soup = BeautifulSoup(requests.get(site).text,'lxml')
        count = [int(count['href'].split("=")[-1]) for count in soup.find_all('a',href=True) if 'pgno' in count['href']]
        self.publications_count = max(count)

        # Pdf pages
        site = 'https://www.al-watan.com/pdf'
        soup = BeautifulSoup(requests.get(site).text, 'lxml')
        count = [int(count['href'].split("=")[-1]) for count in soup.find_all('a', href=True) if 'pgno' in count['href']]
        self.maximum = max(count)

    # The following method will download all the pdfs for a particular page
    def download_pdfs_page(self,page_number:int):
        if 1 <= page_number <= self.maximum:
            site = f'https://www.al-watan.com/PDF?pgno={page_number}'
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = ['https://www.al-watan.com'+pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1].split("?")[0]
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")


    # The following method will download all the publications for a particular page
    def download_publications_page(self,page_number:int):
        if 1 <= page_number <= self.publications_count:
            site = f'https://www.al-watan.com/اصدارات?pgno={page_number}'
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = set(list(['https://www.al-watan.com' + pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]))
            for pdf in pdfs:
                filename = pdf.split("/")[-1].split("?")[0]
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"{filename}", 'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one page to another later page for pdfs
    def download_pdfs_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.download_pdfs_page(n1)
            n1 += 1


    # The following method will download all the pdfs from one page to another later page for publications
    def download_publications_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.download_publications_page(n1)
            n1 += 1

    # The following method will download all the pdfs
    def download_all_pdfs(self):
        self.download_pdfs_n1_n2(1,self.maximum)

    # The following method will download all the publications
    def download_all_publications(self):
        self.download_publications_n1_n2(1,self.publications_count)

    # The following method will check if all the pdfs for a pdf page were downloaded or not
    def check_pdfs_page(self,page_number:int):
        if 1 <= page_number <= self.maximum:
            site = f'https://www.al-watan.com/PDF?pgno={page_number}'
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = ['https://www.al-watan.com' + pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                filename = pdf.split("/")[-1].split("?")[0]
                if filename not in os.listdir():
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{filename} was already downloaded")

    # The following method will check all the publications for a particular page
    def check_publications_page(self, page_number: int):
        if 1 <= page_number <= self.publications_count:
            site = f'https://www.al-watan.com/اصدارات?pgno={page_number}'
            soup = BeautifulSoup(requests.get(url=site).text, 'lxml')
            pdfs = set(list(['https://www.al-watan.com' + pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]))
            for pdf in pdfs:
                filename = pdf.split("/")[-1].split("?")[0]
                if filename not in os.listdir():
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}")
                else:
                    print(f"{filename} was already downloaded")

    # The following method will check from one page to another later page for pdfs
    def check_pdfs_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.check_pdfs_page(n1)
            n1 += 1

    # The following method will check all the pdfs from one page to another later page for publications
    def check_publications_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        while n1 <= n2:
            self.check_publications_page(n1)
            n1 += 1

    # The following method will download all the pdfs
    def check_all_pdfs(self):
        self.check_pdfs_n1_n2(1, self.maximum)

    # The following method will download all the publications
    def check_all_publications(self):
        self.download_publications_n1_n2(1, self.publications_count)

    # The following method will print out the pdfs page count
    def print_pdfs(self):
        print(self.maximum)

    # This method will print out the publications page count
    def print_publications(self):
        print(self.publications_count)

if __name__ == '__main__':
    awq = AlWatanQatar()
    awq.check_all_publications()
