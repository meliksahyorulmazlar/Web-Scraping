# Gulf Weekly, Bahrain

import requests,os,lxml
from bs4 import BeautifulSoup



class GulfWeekly:
    def __init__(self):
        self.start_volume_issue = 16,36
        self.last_volume = self.return_last_volume()


    # The following method will find the lastest volume
    def return_last_volume(self):
        website = 'https://www.gulfweekly.com'
        soup = BeautifulSoup(requests.get(website).text,'lxml')
        pdfs = [pdf['href'].split("/")[1] for pdf in soup.find_all('a',href=True) if 'gulfweekly.pdf' in pdf['href']]
        number = [int(n) for n in pdfs[0].split("_")]
        return number[0],number[1]

    # The following method will download the entire archive
    def download_all(self):
        t = self.start_volume_issue

        if self.last_volume[1] < 52:
            last = self.last_volume[0],self.last_volume[1]+1
        else:
            last = self.last_volume[0]+1,1

        while t != last:
            print(t)
            website = f'https://www.gulfweekly.com/source/{t[0]}_{t[1]}/gulfweekly.pdf'
            pdf_name = f"{t[0]}_{t[1]}.pdf"
            response = requests.get(website)
            if response.status_code == 200:
                with open(f"{pdf_name}",'wb') as f:
                    f.write(response.content)
                with open(f"download_results.txt",'a') as f:
                    f.write(f"{pdf_name} was downloaded.\n")
                print(f"{pdf_name} was downloaded.")
            else:
                with open(f"download_results.txt",'a') as f:
                    f.write(f"{pdf_name} was not downloaded, it had response status code {response.status_code}\n")
                print(f"{pdf_name} was not downloaded, it had response status code {response.status_code}")

            if t[1] < 52:
                t = t[0],t[1]+1
            elif t[1] == 52:
                t = t[0]+1,1

    # The following method will check the entire archive
    def check_all(self):
        t = self.start_volume_issue

        if self.last_volume[1] < 52:
            last = self.last_volume[0], self.last_volume[1] + 1
        else:
            last = self.last_volume[0] + 1, 1

        while t != last:
            print(t)
            website = f'https://www.gulfweekly.com/source/{t[0]}_{t[1]}/gulfweekly.pdf'
            pdf_name = f"{t[0]}_{t[1]}.pdf"
            if pdf_name not in os.listdir():
                response = requests.get(website)
                if response.status_code == 200:
                    with open(f"{pdf_name}", 'wb') as f:
                        f.write(response.content)
                    with open(f"download_results.txt", 'a') as f:
                        f.write(f"{pdf_name} was downloaded.\n")
                    print(f"{pdf_name} was downloaded.")
                else:
                    with open(f"download_results.txt", 'a') as f:
                        f.write(f"{pdf_name} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{pdf_name} was not downloaded, it had response status code {response.status_code}")
            else:
                print(f"{pdf_name} was already downloaded.")

            if t[1] < 52:
                t = t[0], t[1] + 1
            elif t[1] == 52:
                t = t[0] + 1, 1

if __name__ == "__main__":
    gulf_weekly = GulfWeekly()
    gulf_weekly.check_all()