#Webscraping pdfs of the national library of Azerbaijan
#The main page is www.millikitabxana.az


import requests,os,lxml,json,unicodedata
from bs4 import BeautifulSoup


class AzerbaijanLibrary:
    def __init__(self):
        self.newspapers_site = "https://www.millikitabxana.az/newspapers"
        self.journals_site = "https://www.millikitabxana.az/journals"
        self.newspapers = []
        self.journals = []
        self.get_newspapers()
        self.get_journals()

    # Changes the Russian text etc.
    def normalize_text(self,text):
        return unicodedata.normalize('NFC', text.strip()).title()

    #This method will find all the newspapers on the website
    def get_newspapers(self):
        soup = BeautifulSoup(requests.get(url=self.newspapers_site).text,"lxml")
        select_tag = soup.find("select",class_="form-control")
        newspapers = [name.text.replace("/","-") for name in select_tag.find_all("option")][1:]
        for n in newspapers:
            n = self.normalize_text(n)
            if n not in self.newspapers:
                self.newspapers.append(n)
        print(self.newspapers)


    #This method will find all the journals on the website
    def get_journals(self):
        soup = BeautifulSoup(requests.get(url=self.journals_site).text, "lxml")
        select_tag = soup.find("select", class_="form-control")
        journals = [name.text for name in select_tag.find_all("option")][1:]
        for n in journals:
            n = self.normalize_text(n)
            if n not in self.journals:
                self.journals.append(n)
            else:
                print(n)
        print(self.journals)

    #This method will show all the newspaper names
    def show_newspapers(self):
        print(self.newspapers)

    #This method will show all the journal names
    def show_journals(self):
        print(self.journals)

    #This method will return how many pages a newspaper/journal has
    #If it has less than 12, it will have 1 page
    #If the count is exactly divisible by 12 it will n/12 pages
    #Otherwise it will have n//12 +1 pages
    def check_pages(self,count:int):
        if count <=12:
            return 1
        elif count % 12 == 0:
            return count//12
        else:
            return count//12 + 1

    #The following method will download all the newspapers on the archive
    def download_newspapers(self):
        for newspaper in self.newspapers:
            self.download_newspaper(newspaper)

    #This method will download all the journals on the archive
    def download_journals(self):
        for journal in self.journals:
            self.download_journal(journal)

    #This method will download the journal/newspaper
    def download(self,name:str,pdf_link:str,date:str):
        type = ""
        if "newspapers" in pdf_link:
            type = "Newspapers"
            try:
                os.mkdir(f"Newspapers")
            except FileExistsError:
                pass
        
        if "journals" in pdf_link:
            type = "Journals"
            try:
                os.mkdir(f"Journals")
            except FileExistsError:
                pass
                
        
        if type == "Journals" and "/" in name:
            name = name.replace("/","-")
            date = date.replace("/","-")
        file_name = f"{name}-{date}.pdf"
        try:
            os.makedirs(f"{type}/{name}")
        except FileExistsError:
            pass

        response = requests.get(url=pdf_link)
        if response.status_code == 200:
            with open(f"{type}/{name}/{file_name}", "wb") as f:
                f.write(response.content)
            if type == "Journals":
                with open("journal_results.txt", "a") as f:
                    f.write(f"{file_name} was downloaded\n")
            else:
                with open("newspaper_results.txt", "a") as f:
                    f.write(f"{file_name} was downloaded\n")
            print(f"{file_name} was downloaded")
        else:
            if type == "Journals":
                with open("journal_results.txt", "a") as f:
                    f.write(f"{file_name} was not downloaded,it had response status code {response.status_code}\n")
            else:
                with open("newspaper_results.txt", "a") as f:
                    f.write(f"{file_name} was not downloaded,it had response status code {response.status_code}\n")
            print(f"{file_name} was not downloaded,it had response status code {response.status_code}")


    # This method will download a specific journal's archive
    def download_journal(self,journal:str):
        if journal in self.journals:
            website = f"https://www.millikitabxana.az/newspapers/search?name={journal}&year=&month="
            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            print([s.text for s in soup.find_all("span")], journal)
            items = [s.text for s in soup.find_all("span")]
            item = items[4]
            number = 1
            if item != '[email\xa0protected]':
                number = int(item)
            page_count = self.check_pages(count=number)
            pdfs = []
            dates = []
            for i in range(1,page_count+1):
                webpage = f"https://www.millikitabxana.az/journals/search?name={journal}&date=&number=&page={i}"
                soup = BeautifulSoup(requests.get(url=webpage).text,"lxml")
                new_pdfs = [pdf["source"] for pdf in soup.find_all("a",source=True,download=True,class_="_df_custom")]
                new_dates = [div.text.strip() for div in soup.find_all("div",class_="date")][1:]

                for i in range(len(new_pdfs)):
                    new_pdf = new_pdfs[i]
                    date = new_dates[i]
                    if len(date) == 0:
                        date = new_pdf.split("/")[-1]
                    pdfs.append(new_pdf)
                    dates.append(date)

            for i in range(len(pdfs)):
                pdf_link = pdfs[i]
                if pdf_link == "www.millikitabxana.az":
                    print(journal)
                date = dates[i]
                self.download(name=journal, pdf_link=pdf_link, date=date)
                try:
                    with open("journal_results.json", "r") as f:
                        journal_dictionary = json.load(f)
                except FileNotFoundError:
                    with open("journal_results.json", "w") as f:
                        json.dump({}, f, indent=4)
                        journal_dictionary = {}
                if journal in journal_dictionary:
                    journal_list = journal_dictionary[journal]
                    journal_list.append(pdf_link)
                    journal_dictionary[journal] = journal_list
                else:
                    journal_dictionary[journal] = [pdf_link]

                with open("journal_results.json", "w") as f:
                    json.dump(journal_dictionary, f, indent=4, ensure_ascii=False)


    #This method will download all the newspaper's archive
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            website = f"https://www.millikitabxana.az/newspapers/search?name={newspaper}&year=&month="
            soup = BeautifulSoup(requests.get(url=website).text,"lxml")
            number = int([s.text for s in soup.find_all("span")][4])
            page_count = self.check_pages(count=number)
            pdfs = []
            dates = []
            for i in range(1, page_count + 1):
                webpage = f"https://www.millikitabxana.az/newspapers/search?name={newspaper}&date=&number=&page={i}"
                soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
                new_pdfs = [pdf["source"] for pdf in soup.find_all("a", source=True,download=True,class_="_df_custom")]
                new_dates = [div.text.strip() for div in soup.find_all("div", class_="date") if "İl" not in div.text and "Ay" not in div.text]
                new_dates = [date for date in new_dates if "pdf" not in date and date != ""]

                for i in range(len(new_pdfs)):
                    new_pdf = new_pdfs[i]
                    date = new_dates[i]
                    if len(date) == 0:
                        date = new_pdf.split("/")[-1]
                    pdfs.append(new_pdf)
                    dates.append(date)

            for i in range(len(pdfs)):
                pdf_link = pdfs[i]
                date = dates[i]
                self.download(name=newspaper, pdf_link=pdf_link, date=date)

                try:
                    with open("newspaper_results.json", "r") as f:
                        newspaper_dictionary = json.load(f)
                except FileNotFoundError:
                    with open("newspaper_results.json", "w") as f:
                        json.dump({}, f, indent=4)
                        newspaper_dictionary = {}
                if newspaper in newspaper_dictionary:
                    newspaper_list = newspaper_dictionary[newspaper]
                    newspaper_list.append(pdf_link)
                    newspaper_dictionary[newspaper] = newspaper_list
                else:
                    newspaper_dictionary[newspaper] = [pdf_link]

                with open("newspaper_results.json", "w") as f:
                    json.dump(newspaper_dictionary, f, indent=4,ensure_ascii=False)

    #After some time if new newspapers have been added to a newspaper on the website's archive
    #You can use this method, and it will find the new newspapers that have been added
    #You just have to keep json file and that's it
    def update_newspaper(self, newspaper: str):
        if newspaper in self.newspapers:
            website = f"https://www.millikitabxana.az/newspapers/search?name={newspaper}&year=&month="
            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            number = int([s.text for s in soup.find_all("span")][4])
            page_count = self.check_pages(count=number)
            pdfs = []
            dates = []
            for i in range(1, page_count + 1):
                webpage = f"https://www.millikitabxana.az/newspapers/search?name={newspaper}&date=&number=&page={i}"
                soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
                new_pdfs = [pdf["source"] for pdf in soup.find_all("a", source=True, download=True, class_="_df_custom")]
                new_dates = [div.text.strip() for div in soup.find_all("div", class_="date") if "İl" not in div.text and "Ay" not in div.text]
                new_dates = [date for date in new_dates if "pdf" not in date and date != ""]


                for new_pdf in new_pdfs:
                    pdfs.append(new_pdf)
                for date in new_dates:
                    dates.append(date)
            print(pdfs)
            print(dates)
            try:
                with open("newspaper_results.json", "r") as f:
                    newspaper_dictionary = json.load(f)
            except FileNotFoundError:
                with open("newspaper_results.json", "w") as f:
                    json.dump({}, f, indent=4)
                    newspaper_dictionary = {}

            if newspaper not in newspaper_dictionary:
                self.download_newspaper(newspaper)
            else:
                newspapers = newspaper_dictionary[newspaper]
                pdfs_to_download = [pdf for pdf in pdfs if pdf not in newspapers]
                print(pdfs_to_download)
                dates_to_download = []

                for pdf in pdfs_to_download:
                    index = pdfs.index(pdf)
                    date_to_add = dates[index]
                    dates_to_download.append(date_to_add)
                print(dates_to_download)

                for i in range(len(pdfs_to_download)):
                    pdf_link = pdfs_to_download[i]
                    date = dates_to_download[i]
                    self.download(name=newspaper, pdf_link=pdf_link, date=date)
                    try:
                        with open("newspaper_results.json", "r") as f:
                            newspaper_dictionary = json.load(f)
                    except FileNotFoundError:
                        with open("newspaper_results.json", "w") as f:
                            json.dump({}, f, indent=4)
                            newspaper_dictionary = {}
                    if newspaper in newspaper_dictionary:
                        newspaper_list = newspaper_dictionary[newspaper]
                        newspaper_list.append(pdf_link)
                        newspaper_dictionary[newspaper] = newspaper_list
                    else:
                        newspaper_dictionary[newspaper] = [pdf_link]

                    with open("newspaper_results.json", "w") as f:
                        json.dump(newspaper_dictionary, f, indent=4, ensure_ascii=False)

    # After some time if new journals have been added to a journal on the website's archive
    # You can use this method, and it will find the new newspapers that have been added
    # You just have to keep json file and that's it
    def update_journal(self, journal: str):
        if journal in self.journals:
            website = f"https://www.millikitabxana.az/journals/search?name={journal}&year=&month="
            soup = BeautifulSoup(requests.get(url=website).text, "lxml")
            number = int([s.text for s in soup.find_all("span")][4])
            page_count = self.check_pages(count=number)
            pdfs = []
            dates = []
            for i in range(1, page_count + 1):
                webpage = f"https://www.millikitabxana.az/journals/search?name={journal}&date=&number=&page={i}"
                soup = BeautifulSoup(requests.get(url=webpage).text, "lxml")
                new_pdfs = [pdf["source"] for pdf in soup.find_all("a", source=True, download=True, class_="_df_custom")]
                new_dates = [div.text.strip() for div in soup.find_all("div", class_="date")][1:]

                for new_pdf in new_pdfs:
                    pdfs.append(new_pdf)
                for date in new_dates:
                    dates.append(date)
            try:
                with open("journal_results.json", "r") as f:
                    journal_dictionary = json.load(f)
            except FileNotFoundError:
                with open("journal_results.json", "w") as f:
                    json.dump({}, f, indent=4)
                    journal_dictionary = {}

            if journal not in journal_dictionary:
                self.download_journal(journal)
            else:
                journals = journal_dictionary[journal]
                pdfs_to_download = [pdf for pdf in pdfs if pdf not in journals]
                dates_to_download = []


                for pdf in pdfs_to_download:
                    index = pdfs.index(pdf)
                    date_to_add = dates[index]
                    dates_to_download.append(date_to_add)


                for i in range(len(pdfs_to_download)):
                    pdf_link = pdfs_to_download[i]
                    date = dates_to_download[i]
                    self.download(name=journal, pdf_link=pdf_link, date=date)
                    try:
                        with open("journal_results.json", "r") as f:
                            journals_dictionary = json.load(f)
                    except FileNotFoundError:
                        with open("journal_results.json", "w") as f:
                            json.dump({}, f, indent=4)
                            journals_dictionary = {}
                    journal = journal.replace("/","-")
                    if journal in journals_dictionary:
                        journal_list = journals_dictionary[journal]
                        journal_list.append(pdf_link)
                        journals_dictionary[journal] = journal_list
                    else:
                        journals_dictionary[journal] = [pdf_link]

                    with open("journal_results.json", "w") as f:
                        json.dump(journals_dictionary, f, indent=4,ensure_ascii=False)

    #The following method will update the contents of all the newspapers
    #You just have to keep the json file
    def update_newspapers(self):
        for newspaper in self.newspapers:
            self.update_newspaper(newspaper)

    #The following method will update the contents of all the journals
    #You just have to keep the json file
    def update_journals(self):
        for journal in self.journals:
            self.update_journal(journal)


if __name__ == "__main__":
    al = AzerbaijanLibrary()

    #Show all the Journals and newspapers

    #This will show all the newspapers
    al.show_newspapers()

    #This will show all the journals
    al.show_journals()

    #The following method will download a specific newspaper given its name
    #You can get the name from show_newspapers() method

    #This will download the newspaper named Hilal
    al.download_newspaper("Hilal")

    # The following method will download a specific journal given its name
    # You can get the name from show_journals() method

    #This will download the journal named Kirpi
    al.download_journal("Kirpi")

    #The following method will download all the newspapers
    al.download_newspapers()

    #The following method will update a specific newspaper

    #I made this method because they update the website and new newspapers might get added
    #This method will know which pdfs are the new ones

    al.update_newspaper("Hilal")

    # I made this method because they update the website and new journals might get added
    # This method will know which pdfs are the new ones

    al.update_journal("Kirpi")

    #The following method will update all the newspapers
    al.update_newspapers()

    #The following method will update the journals
    al.update_journals()


