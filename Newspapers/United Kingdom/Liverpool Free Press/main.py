# Liverpool Free Press Archive

import requests,os,lxml
from bs4 import BeautifulSoup

class LiverpoolFreePress:
    def __init__(self):
        self.site = 'https://freepressarchive.com/issues/archives.html'

    def check_papers(self):
        soup = BeautifulSoup(requests.get(url=self.site).text,'lxml')
        sites = [f"https://freepressarchive.com/issues/{site['href']}" for site in soup.find_all('a',href=True) if 'issue' in site['href']]
        for site in sites:
            new_soup = BeautifulSoup(requests.get(url=site).text,'lxml')
            pdfs = [pdf['href'] for pdf in new_soup.find_all('a',href=True) if '.pdf' in pdf['href']]
            paper_number = site.split("issue")[-1].replace(".html",'')
            try:
                os.mkdir(paper_number)
            except FileExistsError:
                pass
            for pdf in pdfs:
                filename = pdf.split("/")[-1]
                pdf = f'https://freepressarchive.com/issues/{pdf}'
                if filename not in os.listdir(paper_number):
                    response = requests.get(url=pdf)
                    if response.status_code == 200:
                        with open(f'{paper_number}/{filename}','wb') as f:
                            f.write(response.content)
                        with open('download_results.txt','a') as f:
                            f.write(f"{paper_number}/{filename} was downloaded.\n")
                        print(f"{paper_number}/{filename} was downloaded.")
                    else:
                        with open('download_results.txt','a') as f:
                            f.write(f"{paper_number}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(f"{paper_number}/{filename} was not downloaded,it had response status code {response.status_code}")

if __name__ == "__main__":
    lfp = LiverpoolFreePress()
    lfp.check_papers()