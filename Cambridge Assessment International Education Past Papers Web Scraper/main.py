# code to download CAIE past papers (back exams) for students to get all the back exams they need for their exams

import requests,lxml,os
from bs4 import BeautifulSoup

class DownloadPapers:
    def __init__(self):
        self.websites = ["https://pastpapers.co/cie/?dir=A-Level", "https://pastpapers.co/cie/?dir=IGCSE","https://pastpapers.co/cie/?dir=O-Level", "https://pastpapers.co/cie/?dir=Pre-U"]
        self.years = ["2000", "2001", "2002", "2003", '2004', "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012","2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]



    #this downloads all the a-level,igcse,pre-u,o-level past paper (back exams)
    def download_all(self)->None:

        for website in self.websites:

            topics_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            qualification = website.split("=")[-1].replace("%20", " ").replace("%26", "&")
            os.makedirs(qualification)
            topics = [f'https://pastpapers.co/cie/{topic["href"]}' for topic in topics_soup.find_all(name="a", class_="clearfix") if topic["href"] != 'https://pastpapers.co/cie/']

            for topic in topics:

                years_soup = BeautifulSoup(requests.get(url=topic).text, "lxml")
                subject_name = topic.split("/")[-1].replace("%20", " ").replace("%26", "&")
                os.makedirs(f"{qualification}/{subject_name}")
                times = [f'https://pastpapers.co/cie/{time["href"]}' for time in years_soup.find_all(name="a", class_="clearfix") if time["href"] not in self.websites]
                print(times)

                for time in times:

                    final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                    papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in final_soup.find_all("a", class_="clearfix")][:-1]
                    session = time.split("/")[-1].replace("%20", " ").replace("%26", "&")

                    if session in self.years:

                        times = [paper.replace("%20", " ") for paper in papers if "pdf" not in paper]

                        for time in times:

                            final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                            papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in final_soup.find_all("a", class_="clearfix")][:-1]
                            print(papers)
                            session = time.split("/")[-1].replace("%20", " ")
                            os.makedirs(f"{qualification}/{subject_name}/{session}")

                            for paper in papers:

                                paper_name = paper.split("/")[-1].replace("%20", " ").replace("%26", "&")
                                with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                                    f.write(requests.get(url=paper).content)
                                    print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")

                    else:
                        os.makedirs(f"{qualification}/{subject_name}/{session}")
                        for paper in papers:

                            print(paper)
                            paper_name = paper.split("/")[-1]
                            with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                                f.write(requests.get(url=paper).content)
                                print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")

    #this shows all the topics
    def show_topics(self) -> None:
        for website in self.websites:

            print(website.split("=")[-1])
            topics_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            topics = [f'https://pastpapers.co/cie/{topic["href"]}' for topic in topics_soup.find_all(name="a", class_="clearfix") if topic["href"] != 'https://pastpapers.co/cie/']
            print(topics)

    #when given the qualification and the subject name it will download all that subject's past papers
    #You need to get the end of the url from pastpapers.co
    #for example for https://pastpapers.co/cie/?dir=IGCSE/Information%20and%20Communication%20Technology%20%289-1%29%20%280983%29
    #for the qualification igcse will be good enough
    #but the subject name needs to be exactly Information%20and%20Communication%20Technology%20%289-1%29%20%280983%29 the same
    #Example
    #dp = DownloadPapers()
    #dp.download_subject("igcse","Information%20and%20Communication%20Technology%20%289-1%29%20%280983%29")

    def download_subject(self,qualification: str, subject_name: str)->None:

        if qualification.lower() == "igcse":
            qualification = qualification.upper()
        else:
            qualification = qualification.title()

        website = f"https://pastpapers.co/cie/?dir={qualification}"
        link = f"https://pastpapers.co/cie/?dir={qualification}/{subject_name}"
        soup = BeautifulSoup(requests.get(url=link).text, "lxml")
        times = [f'https://pastpapers.co/cie/{time["href"]}' for time in soup.find_all(name="a", class_="clearfix") if time["href"] != website]

        if times == self.websites:
            print("The qualification or the subject name is wrong")
        else:
            os.makedirs(qualification)
            os.makedirs(f"{qualification}/{subject_name}")

            for time in times:

                final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in final_soup.find_all("a", class_="clearfix")][:-1]
                session = time.split("/")[-1].replace("%20", " ").replace("%26", "&")

                if session in self.years:
                    times = [paper.replace("%20", " ") for paper in papers if "pdf" not in paper]

                    for time in times:

                        final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                        papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in final_soup.find_all("a", class_="clearfix")][:-1]
                        print(papers)
                        session = time.split("/")[-1].replace("%20", " ")
                        os.makedirs(f"{qualification}/{subject_name}/{session}")

                        for paper in papers:
                            paper_name = paper.split("/")[-1].replace("%20", " ").replace("%26", "&")
                            with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                                f.write(requests.get(url=paper).content)
                                print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")
                else:
                    os.makedirs(f"{qualification}/{subject_name}/{session}")
                    for paper in papers:

                        print(paper)
                        paper_name = paper.split("/")[-1]
                        with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                            f.write(requests.get(url=paper).content)
                            print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")

    #this will download a specific qualification
    #you just need the name of the qualification right letter wise so "O-LEVEL" or "o-level" will be fine
    def download_qualification(self,name: str)->None:
        qualifications = ["a-level", "igcse", "o-level", "pre-u"]

        if name.lower() in qualifications:
            qualification = name.title()

            if name.lower() == "igcse":
                qualification = name.upper()

            os.makedirs(qualification)
            website = f"https://pastpapers.co/cie/?dir={qualification}"
            topics_soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            topics = [f'https://pastpapers.co/cie/{topic["href"]}' for topic in topics_soup.find_all(name="a", class_="clearfix") if topic["href"] != 'https://pastpapers.co/cie/']

            for topic in topics:

                years_soup = BeautifulSoup(requests.get(url=topic).text, "lxml")
                subject_name = topic.split("/")[-1].replace("%20", " ").replace("%26", "&")
                os.makedirs(f"{qualification}/{subject_name}")
                times = [f'https://pastpapers.co/cie/{time["href"]}' for time in
                         years_soup.find_all(name="a", class_="clearfix") if time["href"] != website]
                print(times)

                for time in times:

                    final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                    papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in
                              final_soup.find_all("a", class_="clearfix")][:-1]
                    session = time.split("/")[-1].replace("%20", " ").replace("%26", "&")

                    if session in self.years:
                        times = [paper.replace("%20", " ") for paper in papers if "pdf" not in paper]

                        for time in times:

                            final_soup = BeautifulSoup(requests.get(url=time).text, "lxml")
                            papers = [f'https://pastpapers.co/cie/{a["href"]}' for a in
                                      final_soup.find_all("a", class_="clearfix")][:-1]
                            print(papers)
                            session = time.split("/")[-1].replace("%20", " ")
                            os.makedirs(f"{qualification}/{subject_name}/{session}")

                            for paper in papers:
                                paper_name = paper.split("/")[-1].replace("%20", " ").replace("%26", "&")
                                with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                                    f.write(requests.get(url=paper).content)
                                    print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")
                    else:
                        os.makedirs(f"{qualification}/{subject_name}/{session}")
                        for paper in papers:

                            print(paper)
                            paper_name = paper.split("/")[-1]
                            with open(f"{qualification}/{subject_name}/{session}/{paper_name}", "wb") as f:
                                f.write(requests.get(url=paper).content)
                                print(f"{qualification}/{subject_name}/{session}/{paper_name} was downloaded")
        else:
            print("The qualification name is wrong")

if __name__ == "__main__":
    dp = DownloadPapers()
    #dp.download_subject("igcse","Information%20and%20Communication%20Technology%20%289-1%29%20%280983%29")
