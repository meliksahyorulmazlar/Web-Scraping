# Lisbon Municipial Library Archive

import requests,lxml,os
from bs4 import BeautifulSoup


class LisbonMuncipialLibrary:
    def __init__(self):
        self.letters = ["A"]
        self.get_letters()
        self.newspapers = []
        self.links = []
        self.find_newspapers()

    # The following method will finf which letters have a
    def get_letters(self):
        website = "https://hemerotecadigital.cm-lisboa.pt/Indice/IndiceA.htm"
        soup = BeautifulSoup(requests.get(url=website).text,"lxml")

        for link in soup.find_all("a",href=True):
            if "Indice" in link["href"]:
                self.letters.append(link.text.strip())

    # The following method will replace text so that it can get the newspaper's names right
    def replace_text(self,string:str)->str:
        return string.replace("\n","").replace("\r","").replace("\t","")

    # The following method will get the href/ the link for newspaper
    def replace_href(self,string:str)->str:
        return string.strip("..")

    # The following method will find all the newspapers on the Lisbon Municipial Library archive
    def find_newspapers(self):
        for letter in self.letters:
            website = f"https://hemerotecadigital.cm-lisboa.pt/Indice/Indice{letter}.htm"

            soup = BeautifulSoup(requests.get(url=website).text,"lxml")

            for link in soup.find_all("a",href=True):
                if link.text.strip() and "Periodicos" in link["href"]:
                    newspaper = self.replace_text(link.text)

                    link = self.replace_href(string=link["href"])
                    link = f"https://hemerotecadigital.cm-lisboa.pt{link}"
                    extension = link.split("/")[-2]
                    newspaper = f"{newspaper}"
                    if link in self.links:
                        self.newspapers[-1] += newspaper
                        if self.newspapers.count(self.newspapers[-1]) == 2:
                            self.newspapers[-1] += f" {extension}"
                    elif newspaper in self.newspapers:
                        newspaper = f"{newspaper} {extension}"
                        self.newspapers.append(newspaper)
                        self.links.append(link)
                    else:
                        self.newspapers.append(newspaper)
                        self.links.append(link)
        for i in range(len(self.newspapers)):
            n = self.newspapers[i]
            self.newspapers[i] = n.replace(":",'')


    #The following method will print the names of all the newspapers
    def print_newspapers(self):
        print(len(self.newspapers))
        print(len(self.links))
        for i in range(len(self.links)):
            print([self.newspapers[i],self.links[i]])

    #The following method will download a newspaper if it is in on the website
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            os.mkdir(newspaper)
            index = self.newspapers.index(newspaper)
            website = self.links[index]
            name_part = website.split("/")[4]
            print(name_part)
            html_part: list = website.split("/")
            print(html_part)
            html_part.pop()
            html_part = "/".join(html_part)


            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            pdf_links = [f"{html_part}/{link['href']}" for link in soup.find_all("a",href=True) if ".pdf" in link['href'] or ".PDF" in link["href"]]

            if len(pdf_links) > 1:
                print("option 1")
                print(pdf_links)
                for pdf in pdf_links:
                    response = requests.get(url=pdf)
                    part1 = pdf.split("/")[-2]
                    part2 = pdf.split("/")[-1]
                    filename = f"{part1} {part2}"
                    if response.status_code == 200:
                        with open(f"{newspaper}/{filename}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{newspaper}/{filename} was downloaded\n")
                        print(f"{newspaper}/{filename} was downloaded\n")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{newspaper}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                        print(
                            f"{newspaper}/{filename} was not downloaded,it had response status code {response.status_code}\n")

            elif len(pdf_links) == 1:
                print("option 2")
                html_links = [f"{html_part}/{link['href']}" for link in soup.find_all("a",href=True) if ("htm" in link["href"] or "HTM" in link["href"]) and "/" not in link["href"]]
                print(pdf_links,newspaper,website,html_links)
                print(len(html_links))
                if len(html_links) == 0:
                    print("option 2a")
                    for pdf in pdf_links:
                        response = requests.get(url=pdf)
                        part1 = pdf.split("/")[-2]
                        part2 = pdf.split("/")[-1]
                        filename = f"{part1} {part2}"
                        if response.status_code == 200:
                            with open(f"{newspaper}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{newspaper}/{filename} was downloaded\n")
                            print(f"{newspaper}/{filename} was downloaded\n")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"{newspaper}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{newspaper}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                else:
                    print("option 2b")
                    links = []
                    for directory in html_links:
                        if directory not in links:
                            links.append(directory)
                    html_links = links
                    for directory in html_links:
                        directory_name = directory.split("/")[-1]
                        directory_name = directory_name.replace(".htm","").replace(".HTM","")
                        os.mkdir(f"{newspaper}/{directory_name}")

                        soup = BeautifulSoup(requests.get(url=directory).text,"lxml")
                        pdf_links = [f"https://hemerotecadigital.cm-lisboa.pt/Periodicos/{name_part}/{link['href'].replace('../','')}" for link in soup.find_all("a",href=True) if ".pdf" in link['href'] or ".PDF" in link["href"]]
                        print(pdf_links)
                        for pdf in pdf_links:
                            response = requests.get(url=pdf)
                            part1 = pdf.split("/")[-2]
                            part2 = pdf.split("/")[-1]
                            filename = f"{part1} {part2}"
                            if response.status_code == 200:
                                with open(f"{newspaper}/{directory_name}/{filename}", "wb") as f:
                                    f.write(response.content)
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{newspaper}/{directory_name}/{filename} was downloaded\n")
                                print(f"{newspaper}/{directory_name}/{filename} was downloaded\n")
                            else:
                                with open("download_results.txt", "a") as f:
                                    f.write(f"{newspaper}/{directory_name}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                                print(f"{newspaper}/{directory_name}/{filename} was not downloaded,it had response status code {response.status_code}\n")
            else:
                print("option 3")
                html_part: list = website.split("/")
                html_part.pop()
                html_part = "/".join(html_part)
                html_links = list(sorted(set([f"{html_part}/{link['href']}" for link in soup.find_all("a",href=True) if ("htm" in link["href"] or "HTM" in link["href"]) and "/" not in link["href"]])))
                print(html_links)
                for directory in html_links:
                    directory_name = directory.split("/")[-1]
                    directory_name = directory_name.replace(".htm", "").replace(".HTM", "")
                    os.mkdir(f"{newspaper}/{directory_name}")

                    soup = BeautifulSoup(requests.get(url=directory).text, "lxml")
                    if newspaper == 'Crónica Constitucional de Lisboa':
                        pdf_links = [f"https://hemerotecadigital.cm-lisboa.pt/Periodicos/{name_part}/1833/{link['href']}" for link in soup.find_all("a", href=True) if ".pdf" in link['href'] or ".PDF" in link["href"]]
                    else:
                        pdf_links = [f"https://hemerotecadigital.cm-lisboa.pt/Periodicos/{name_part}/{link['href']}" for link in soup.find_all("a", href=True) if ".pdf" in link['href'] or ".PDF" in link["href"]]
                    for pdf in pdf_links:
                        response = requests.get(url=pdf)
                        part1 = pdf.split("/")[-2]
                        part2 = pdf.split("/")[-1]
                        filename = f"{part1} {part2}"
                        if response.status_code == 200:
                            with open(f"{newspaper}/{directory_name}/{filename}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{newspaper}/{directory_name}/{filename} was downloaded\n")
                            print(f"{newspaper}/{directory_name}/{filename} was downloaded\n")
                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(f"{newspaper}/{directory_name}/{filename} was not downloaded,it had response status code {response.status_code}\n")
                            print(f"{newspaper}/{directory_name}/{filename} was not downloaded,it had response status code {response.status_code}\n")

    # The following method will download all the newspapers
    def download_all(self):
        for n in self.newspapers:
            self.download_newspaper(n)

if __name__ == "__main__":
    lml = LisbonMuncipialLibrary()
    lml.download_all()

