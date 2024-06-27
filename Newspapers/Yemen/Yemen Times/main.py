import requests,lxml,time,os
from bs4 import BeautifulSoup

# yemen_times_previous.txt has the whole 1845 newspaper links
#Out of the 1845, only 1 does not have a link to a pdf to download
#https://yementimes.com/pdf-archives2011-1516xxi-date2011-10-31-20pages/ gets no link
#You end up with 1844 files to download.The download links are found in yemen_times_final.txt


class YemenTimes:
    def download(self):
        with open("yemen_times_final.txt","r") as f:
            download_links = f.readlines()

        download_links = [link.strip('\n') for link in download_links]

        os.makedirs("Yemen Times Newspapers")
        for download_link in download_links:
            response = requests.get(url=download_link)
            filename = download_link.split("/")[-1]

            if response.status_code == 200:
                with open(f"Yemen Times Newspapers/{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded\n")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded, it had response status code {response.status_code}")
                print(f"{filename} was not downloaded, it had response status code {response.status_code}")

if __name__  == "__main__":
    yt = YemenTimes()
    yt.download()