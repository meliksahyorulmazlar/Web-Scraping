import requests,lxml,time,os
from bs4 import BeautifulSoup

# yemen_times_previous.txt has the whole 1845 newspaper links
#Out of the 1845, only 1 does not have a link to a pdf to download
#https://yementimes.com/pdf-archives2011-1516xxi-date2011-10-31-20pages/ gets no link
#You end up with 1844 files to download.The download links are found in yemen_times_final.txt


class YemenTimes:
    def __init__(self):
        with open("yemen_times_final.txt","r") as f:
            download_links = f.readlines()
        self.download_links = [link.strip('\n') for link in download_links]

    # The following method will download all the newspapers
    def download_all(self):
        try:
            os.mkdir("Yemen Times Newspapers")
        except FileExistsError:
            pass
        for download_link in self.download_links:
            response = requests.get(url=download_link)
            filename = download_link.split("/")[-1]

            if response.status_code == 200:
                with open(f"Yemen Times Newspapers/{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}\n")
                print(f"{filename} was not downloaded, it had response status code {response.status_code}")

    #The following method will check if all the pdfs have been downloaded or not. If the code finds a pdf that has not been downloaded, this code will download it.
    def check_all(self):
        try:
            os.mkdir("Yemen Times Newspapers")
        except FileExistsError:
            pass
        for download_link in self.download_links:
            filename = download_link.split("/")[-1]
            if filename not in os.listdir('Yemen Times Newspapers'):
                response = requests.get(url=download_link)
                if response.status_code == 200:
                    with open(f"Yemen Times Newspapers/{filename}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was downloaded.\n")
                    print(f"{filename} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{filename} was not downloaded, it had response status code {response.status_code}.\n")
                    print(f"{filename} was not downloaded, it had response status code {response.status_code}")

if __name__  == "__main__":
    yt = YemenTimes()
    yt.check_all()
