#Webscraper to get the genealogy or the journal of the Dutch Burgher Union Of Ceylon
import requests,os,lxml
from bs4 import BeautifulSoup


class Ceylon:
    def download_genealogy(self):
        name = "Genealogy"
        website = "https://thedutchburgherunion.org/dbu-genealogy/"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")
        pdf_links = sorted(list(set([link["href"] for link in soup.find_all("a",href=True) if "pdf" in link["href"]])))
        os.makedirs(name)
        for pdf in pdf_links:
            filename = pdf.split("/")[-1]
            if "https://"  in pdf:
                url = pdf
            elif "http://" in pdf:
                url = pdf.replace("http://","https://")
            else:
                url = "https://" + pdf
            print(url)
            try:
                response = requests.get(url=url)
            except TimeoutError:
                response = requests.get(url=url)
            if response.status_code == 200:
                with open(f"{name}/{filename}","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt","a") as f:
                    f.write(f"{filename} was not downloaded,with response status code {response.status_code}\n")
                print(f"{filename} was downloaded,with response status code {response.status_code}")

    def download_journal(self):
        name = "Journal"
        website = "https://thedutchburgherunion.org/journal-index/"
        soup = BeautifulSoup(requests.get(url=website).text, "lxml")
        pdf_links = sorted(list(set([link["href"].replace(" ","%20") for link in soup.find_all("a", href=True) if "pdf" in link["href"]])))
        os.makedirs(name)
        for pdf in pdf_links:
            filename = pdf.split("/")[-1]
            if "https://"  in pdf:
                url = pdf
            elif "http://" in pdf:
                url = pdf.replace("http://","https://")
            else:
                url = "https://" + pdf
            print(url)

            response = requests.get(url=url)

            if response.status_code == 200:
                with open(f"{name}/{filename}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{filename} was downloaded\n")
                print(f"{filename} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{filename} was not downloaded,with response status code {response.status_code}\n")
                print(f"{filename} was downloaded,with response status code {response.status_code}")


c = Ceylon()
c.download_genealogy()

