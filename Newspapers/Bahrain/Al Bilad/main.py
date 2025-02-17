# Al Bilad , newspapers from Bahrain

import requests,lxml,os
from bs4 import BeautifulSoup



class AlBiladBahrain:
    def __init__(self):
        self.page_count = self.gather_pages()
        self.minimum_newspapers = 2940
        self.maximum_newspapers = self.find_maximum_page_number()
        try:
            os.mkdir('Supplements')
        except FileExistsError:
            pass
        try:
            os.mkdir('Newspapers')
        except FileExistsError:
            pass

    # The following method will find the maximum newspaper number
    def find_maximum_page_number(self):
        website = f'https://www.albiladpress.com/archive'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pdfs = [int(pdf['href'].split("/")[-1]) for pdf in soup.find_all('a',href=True) if 'pdf' in pdf['href']]
        return max(pdfs)

    # The following method will gather how many pages there are on the archive
    def gather_pages(self):
        website = 'https://www.albiladpress.com/magazines?page=1'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pages = [int(page['href'].split("=")[-1]) for page in soup.find_all('a',href=True) if 'page=' in page['href']]
        return max(pages)

    # The following method will print the page count of the supplements
    def print_supplements_page_count(self):
        print(self.page_count)

    # The following method will print the page count of the supplements
    def print_newspapers_page_count(self):
        print(self.maximum_newspapers)

    # The following method will download a page number
    def download_page_number_supplements(self,number:int):
        if 1 <= number <= self.page_count:
            website = f"https://www.albiladpress.com/magazines?page={number}"

            soup = BeautifulSoup(requests.get(website).text,'lxml')

            magazines = []
            for mag in soup.find_all('a',href=True):
                if '/magazines/' in mag['href'] and mag['href'] not in magazines:
                    magazines.append(mag['href'])

            for mag in magazines:
                soup = BeautifulSoup(requests.get(mag).text,'lxml')
                h2 = soup.find('h2')
                title = h2.text.strip()
                pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
                pdf = pdfs[0]
                code = pdf.split("/")[-3]
                filename = f"{code}-{title}.pdf"

                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"Supplements/{filename}",'wb') as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}.")


    # The following method will download from one number to another number
    def download_n1_n2_supplements(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2):
            self.check_page_number_supplements(i)

    # The following method will download the entire archive
    def download_all_supplements(self):
        self.download_n1_n2_supplements(1,self.page_count)


    # The following method will check if all the pdfs for a page were downloaded or not
    def check_page_number_supplements(self, number: int):
        if 1 <= number <= self.page_count:
            website = f"https://www.albiladpress.com/magazines?page={number}"

            soup = BeautifulSoup(requests.get(website).text, 'lxml')

            magazines = []
            for mag in soup.find_all('a', href=True):
                if '/magazines/' in mag['href'] and mag['href'] not in magazines:
                    magazines.append(mag['href'])

            for mag in magazines:
                soup = BeautifulSoup(requests.get(mag).text, 'lxml')
                h2 = soup.find('h2')
                title = h2.text.strip()
                pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
                pdf = pdfs[0]
                code = pdf.split("/")[-3]
                filename = f"{code}-{title}.pdf"

                if filename not in os.listdir(f"Supplements"):
                    response = requests.get(pdf)
                    if response.status_code == 200:
                        with open(f"Supplements/{filename}", 'wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was downloaded.\n")
                        print(f"{filename} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                        print(f"{filename} was not downloaded, it had response status code {response.status_code}.")
                else:
                    print(f"{filename} was already downloaded")

    # The following method will check from one number to another number
    def check_n1_n2_supplements(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1, n2):
            self.check_page_number_supplements(i)

    # The following method will check the entire archive
    def check_all_supplements(self):
        self.check_n1_n2_supplements(1, self.page_count)

    # The following method will download a specific newspaper issue number
    def download_newspaper_issue(self,number:int):
        if self.minimum_newspapers <= number <= self.maximum_newspapers:
            website = f"https://www.albiladpress.com/pdf-version/1/{number}"
            soup = BeautifulSoup(requests.get(website).text,'lxml')
            filename = f"{number}.pdf"
            pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            pdf = pdfs[0]
            response = requests.get(pdf)
            if response.status_code == 200:
                with open(f"Newspapers/{filename}",'wb') as f:
                    f.write(response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was downloaded.\n")
                print(f"{filename} was downloaded.")
            else:
                with open('download_results.txt','a') as f:
                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    # The following method will download from one issue number to another later issue number
    def download_newspaper_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2):
            self.download_newspaper_issue(i)

    # The following method will download the entire archive
    def download_all(self):
        self.check_n1_n2_supplements(self.minimum_newspapers,self.maximum_newspapers)

    # The following method will check if a specific newspaper issue number has been downloaded or not
    def check_newspaper_issue(self, number: int):
        if self.minimum_newspapers <= number <= self.maximum_newspapers:
            filename = f"{number}.pdf"
            if filename not in os.listdir("Newspapers"):
                website = f"https://www.albiladpress.com/pdf-version/1/{number}"
                soup = BeautifulSoup(requests.get(website).text, 'lxml')
                pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
                pdf = pdfs[0]
                response = requests.get(pdf)
                if response.status_code == 200:
                    with open(f"Newspapers/{filename}", 'wb') as f:
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

    # The following method will check from one issue number to another later issue number
    def check_newspaper_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1, n2):
            self.check_newspaper_issue(i)

    # The following method will check the entire archive
    def check_all_newspapers(self):
        self.check_newspaper_n1_n2(self.minimum_newspapers, self.maximum_newspapers)


if __name__ == "__main__":
    al_bilad = AlBiladBahrain()
    al_bilad.check_newspaper_issue(number=al_bilad.maximum_newspapers)