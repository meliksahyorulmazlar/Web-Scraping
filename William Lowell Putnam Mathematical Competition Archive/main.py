# William Lowell Putnam Mathematical Competition Archive
# the William Lowell Putnam Mathematical Competition is a fun and challenging one-day competitive mathematical examination given in December in the US and Canada where undergraduates compete between universities individually and in teams for recognition, cash prizes, and scholarships.


import requests,lxml,os
from bs4 import BeautifulSoup


class Putnam:
    def __init__(self):
        self.main_page = "https://kskedlaya.org/putnam-archive/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','DNT': '1'}

        response = requests.get(url=self.main_page,headers=self.headers)
        self.soup = BeautifulSoup(response.text,"lxml")
        self.greatest_year = self.find_greatest_year()

    # The following method will find the latest year that the putnam math competition took place
    def find_greatest_year(self)->int:
        texs = self.soup.find_all("a", href=True)
        years = [int(tex['href'].strip(".tex")) for tex in texs if "tex" in tex['href'] and 's' not in tex['href'] and 'Winners' not in tex['href']]
        years = years[::-1]
        return max(years)

    # The following method will download all the problems in the tex format on the archive
    def download_problems_tex(self):
        texs = self.soup.find_all("a", href=True)
        texs = [tex['href'] for tex in texs if "tex" in tex['href'] and 's' not in tex['href'] and 'Winners' not in tex['href']]
        texs = texs[::-1]

        try:
            os.mkdir("Problems (TEX)")
        except FileExistsError:
            pass

        for link in texs:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Problems (PDF)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the problems in the pdf format on the archive
    def download_problems_pdf(self):
        pdfs = self.soup.find_all("a",href=True)
        pdfs = [pdf['href'] for pdf in pdfs if "pdf" in pdf['href'] and 's' not in pdf['href'] and 'Winners' not in pdf['href'] and "Putnam" not in pdf["href"] ]
        pdfs = pdfs[::-1]

        try:
            os.mkdir("Problems (PDF)")
        except FileExistsError:
            pass

        for link in pdfs:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Problems (PDF)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the solutions in the pdf format on the archive
    def download_solutions_pdf(self):
        pdfs = self.soup.find_all("a", href=True)
        pdfs = [pdf['href'] for pdf in pdfs if "pdf" in pdf['href']  and "s" in pdf['href'] and 'Winners' not in pdf['href'] and "Putnam" not in pdf["href"] and "conversation" not in pdf['href']]
        pdfs = pdfs[::-1]

        try:
            os.mkdir("Solutions (PDF)")
        except FileExistsError:
            pass

        for link in pdfs:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Solutions (PDF)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the solutions in the tex format on the archive
    def download_solutions_tex(self):
        texs = self.soup.find_all("a", href=True)
        texs = [tex['href'] for tex in texs if "tex" in tex['href'] and "s" in tex['href'] and 'Winners' not in tex['href'] ]
        texs = texs[::-1]

        try:
            os.mkdir("Solutions (TEX)")
        except FileExistsError:
            pass

        for link in texs:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Solutions (TEX)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the winners in the html format on the archive
    def download_winners_html(self):
        htmls = self.soup.find_all("a", href=True)
        htmls = [html_link['href'] for html_link in htmls if "html" in html_link['href'] and "results" in html_link['href']]
        htmls = htmls[::-1]

        try:
            os.mkdir("Winners (HTML)")
        except FileExistsError:
            pass

        for link in htmls:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Winners (HTML)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the winners in the pdf format on the archive
    def download_winners_pdf(self):
        pdfs = self.soup.find_all("a", href=True)
        pdfs = [pdf['href'] for pdf in pdfs if"pdf" in pdf['href'] and "s" in pdf['href'] and 'Winners'  in pdf['href']]
        pdfs = pdfs[::-1]

        try:
            os.mkdir("Winners (PDF)")
        except FileExistsError:
            pass

        for link in pdfs:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Winners (PDF)/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the scores on the archive
    def download_scores(self):
        htmls = self.soup.find_all("a", href=True)
        htmls = [html_link['href'] for html_link in htmls if "html" in html_link['href'] and "stats" in html_link['href']]
        htmls = htmls[::-1]

        try:
            os.mkdir("Scores")
        except FileExistsError:
            pass

        for link in htmls:
            website = f"https://kskedlaya.org/putnam-archive/{link}"
            response = requests.get(website, headers=self.headers)

            if response.status_code == 200:
                with open(f"Scores/{link}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was downloaded\n")
                print(f"{link} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                print(f"{link} was not downloaded, it had response status code {response.status_code}")

    # The following method will download all the links for a given year between 1985 and the latest year the Putnam math competition was held
    def download_year(self,year:int):
        if 1985 <= year <= self.greatest_year:
            links = self.soup.find_all("a",href=True)
            links = [link["href"] for link in links if f"{year}" in link['href']]

            try:
                os.mkdir(f"{year}")
            except FileExistsError:
                pass

            for link in links:
                website = f"https://kskedlaya.org/putnam-archive/{link}"
                response = requests.get(website,headers=self.headers)

                if response.status_code == 200:
                    with open(f"{year}/{link}","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{link} was downloaded\n")
                    print(f"{link} was downloaded")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{link} was not downloaded,it had response status code {response.status_code}\n")
                    print(f"{link} was not downloaded, it had response status code {response.status_code}")

    #The Following method will download the entire archive
    def download_all(self):
        texs = self.soup.find_all("a", href=True)
        years = [int(tex['href'].strip(".tex")) for tex in texs if"tex" in tex['href'] and 's' not in tex['href'] and 'Winners' not in tex['href']]
        years = years[::-1]
        for year in years:
            self.download_year(year)

if __name__ == "__main__":
    putnam = Putnam()

    # The following method will download the entire archive
    putnam.download_all()

    # The following method will download all the problems in the pdf format on the archive
    putnam.download_problems_pdf()

    # The following method will download all the problems in the tex format on the archive
    putnam.download_problems_tex()

    # The following method will download all the solutions in the pdf format on the archive
    putnam.download_solutions_pdf()

    # The following method will download all the solutions in the tex format on the archive
    putnam.download_solutions_tex()

    # The following method will download all the scores on the archive
    putnam.download_scores()

    # The following method will download all the winners in the pdf format on the archive
    putnam.download_winners_pdf()

    # The following method will download all the winners in the html format on the archive
    putnam.download_winners_html()

    # The following method will download all the links for a given year between 1985 and the latest year the Putnam math competition was held
    #putnam.download_year(1990)
