# Diario Oficial , archive of the official newspaper of the government of El Salvador 1847-1953

import requests,os
from bs4 import BeautifulSoup


class Diario:
    def __init__(self):
        self.directories = []
        self.gather_directories()

    # The following method will gather all the directories on the website
    def gather_directories(self):
        site = 'http://abaco.uca.edu.sv/acervo/Diario_Oficial/'
        soup = BeautifulSoup(requests.get(site).text,'lxml')
        directories = [directory['href'].replace("%20"," ").replace("/","") for directory in soup.find_all('a',href=True) if '.txt' not in directory['href'] and "?" not in directory['href']]
        directories.remove("acervo")
        self.directories = directories


    # The following method will print all the directories that the website has
    def print_directories(self):
        for directory in self.directories:
            print(directory)

    # The following method will download all the pdfs for a particular directory
    def download(self,directory:str):
        if directory in self.directories:
            os.mkdir(directory)
            site = f'http://abaco.uca.edu.sv/acervo/Diario_Oficial/{directory}'
            soup = BeautifulSoup(requests.get(site).text,'lxml')
            pdfs = [pdf['href'] for pdf in soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            for pdf in pdfs:
                response = requests.get(f"{site}/{pdf}")
                if response.status_code == 200:
                    with open(f"{directory}/{pdf}","wb") as f:
                        f.write(response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f"{directory}/{pdf} was downloaded.\n")
                    print(f"{directory}/{pdf} was downloaded.")
                else:
                    with open('download_results.txt','a') as f:
                        f.write(f"{directory}/{pdf} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{directory}/{pdf} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the directories on the website
    def download_all(self):
        for directory in self.directories:
            self.download(directory)

    # The following method will check if all the pdfs for a particular directory were downloaded or not
    def check(self,directory:str):
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
        site = f'http://abaco.uca.edu.sv/acervo/Diario_Oficial/{directory}'
        soup = BeautifulSoup(requests.get(site).text, 'lxml')
        pdfs = [pdf['href'] for pdf in soup.find_all('a', href=True) if '.pdf' in pdf['href']]
        for pdf in pdfs:
            if pdf not in os.listdir(directory):
                response = requests.get(f"{site}/{pdf}")
                if response.status_code == 200:
                    with open(f"{directory}/{pdf}", "wb") as f:
                        f.write(response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{directory}/{pdf} was downloaded.\n")
                    print(f"{directory}/{pdf} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(
                            f"{directory}/{pdf} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{directory}/{pdf} was not downloaded, it had response status code {response.status_code}")
            else:
                print(f"{directory}/{pdf} was already downloaded")

    # The following method will check all the directories
    def check_all(self):
        for directory in self.directories:
            self.check(directory)

if __name__ == "__main__":
    diario = Diario()
    diario.check_all()