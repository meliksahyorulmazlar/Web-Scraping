# Cyprus Press Information Office

import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests,os,lxml
from bs4 import BeautifulSoup



class CyprusPressInformationOffice:
    def __init__(self):
        self.start_driver()
        self.driver.get('https://www.pressarchive.cy/s/en/page/homepage')
        self.newspaper_dictionary = {}
        self.gather_newspapers()

    # The following method starts the selenium webdriver
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach',True)
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    # The following method gathers all the newspapers
    def gather_newspapers(self):
        self.driver.execute_script("window.scrollBy(0, 500);")
        buttons = [b for b in self.driver.find_elements(By.TAG_NAME,'button') if b.text.strip() == 'Accept & Close']
        self.driver.execute_script("arguments[0].scrollIntoView(true);", buttons[0])
        buttons[0].click()

        self.driver.get(url='https://www.pressarchive.cy/s/en/find?q=&limit%5Bresource_class_s%5D%5B0%5D=dctype:Collection')
        self.driver.execute_script("window.scrollBy(0, 1500);")
        pages = self.driver.find_element(By.CLASS_NAME,'page-count')
        page_count = pages.text.replace("of ","")
        for i in range(1,int(page_count)+1):
            site = f'https://www.pressarchive.cy/s/en/find?q=&limit%5Bresource_class_s%5D%5B0%5D=dctype:Collection&page={i}'
            self.driver.get(site)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            names = [p.text.replace('\n', '') for p in soup.find_all('h1') if "\n" in p.text]
            new_papers = [paper['href'] for paper in soup.find_all('a',href=True) if 'q=' in paper['href'] and '%' not in paper['href']]
            new_papers = new_papers[2:-1]

            for i in range(len(new_papers)):
                code = new_papers[i].split("/")[-1].split("?")[0]
                key = f"{names[i].strip()}-{code}"
                value = f"https://www.pressarchive.cy{new_papers[i]}"
                self.newspaper_dictionary[key] = value

    # The following method will download a specific newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            os.mkdir(newspaper)
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            try:
                pages = self.driver.find_element(By.CLASS_NAME, 'page-count')
            except selenium.common.exceptions.NoSuchElementException:
                print('nothing to download')
            else:
                page_count = int(pages.text.replace("of ", ""))
                for i in range(1,page_count+1):
                    site = f"{self.newspaper_dictionary[newspaper]}&page={i}"
                    self.driver.get(site)
                    soup = BeautifulSoup(self.driver.page_source,'lxml')
                    new_dates = [date.text.split(" ")[1] for date in soup.find_all('h5') if '\n' not in date.text]
                    new_links = [link['href'] for link in soup.find_all('a',href=True) if '/s/en/item/' in link['href'] and "#" not in link['href']]
                    print(new_dates)
                    print(new_links)

                    for j in range(len(new_links)):
                        link = f"https://www.pressarchive.cy{new_links[j]}"
                        date = new_dates[i]
                        self.driver.get(url=link)
                        with open('content.txt', 'w') as f:
                            f.write(BeautifulSoup(self.driver.page_source, 'lxml').prettify())
                        code = None
                        with open('content.txt', 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                if 'iiifResourceUri' in line:
                                    list_form = line.split("_")
                                    code = list_form[-1].split("/")[0]
                        if code is None:
                            continue
                        print(code)
                        filename = f"{newspaper}-{date}"
                        print(code, filename)
                        self.check_individual_paper(code, filename, newspaper)


    # The following method will download all the newspapers
    def download_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.download_newspaper(newspaper)

    # This method will check if all the newspapers have been downloaded or not
    def check_newspaper(self,newspaper:str):
        if newspaper in self.newspaper_dictionary:
            try:
                os.mkdir(newspaper)
            except FileExistsError:
                pass
            site = self.newspaper_dictionary[newspaper]
            self.driver.get(site)
            try:
                pages = self.driver.find_element(By.CLASS_NAME, 'page-count')
            except selenium.common.exceptions.NoSuchElementException:
                print('nothing to download')
            else:
                page_count = int(pages.text.replace("of ", ""))
                for i in range(1,page_count+1):
                    print(i)
                    site = f"{self.newspaper_dictionary[newspaper]}&page={i}"
                    self.driver.get(site)
                    soup = BeautifulSoup(self.driver.page_source,'lxml')
                    new_dates = [date.text.split(" ")[1] for date in soup.find_all('h5') if '\n' not in date.text]
                    new_links = [link['href'] for link in soup.find_all('a',href=True) if '/s/en/item/' in link['href'] and "#" not in link['href']]
                    print(new_dates)
                    print(new_links)
                    print(len(new_links))
                    print(len(new_dates))
                    for j in range(len(new_links)):
                        link = f"https://www.pressarchive.cy{new_links[j]}"
                        date = new_dates[j]
                        print(i,j)
                        self.driver.get(url=link)
                        print(self.driver.current_url)
                        with open('content.txt', 'w') as f:
                            f.write(BeautifulSoup(self.driver.page_source, 'lxml').prettify())
                        code = None
                        with open('content.txt', 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                if 'iiifResourceUri' in line:
                                    list_form = line.split("_")
                                    code = list_form[-1].split("/")[0]
                        if code is None:
                            continue
                        print(code)
                        filename = f"{newspaper}-{date}"
                        print(code,filename)
                        if f"{filename}.pdf" not in os.listdir(newspaper) and f"{filename}" not in os.listdir(newspaper):
                            self.check_individual_paper(code,filename,newspaper)
                        elif f'{filename}' in os.listdir(newspaper):
                            self.check_individual_paper(code,filename,newspaper)

    #The following method will download the newspapers
    def check_individual_paper(self,code,filename,newspaper):
        site = f'https://www.pressarchive.cy/files/v2/publication_{code}_1/fullpdf'
        response = requests.get(url=site)
        print(response.status_code)
        if response.status_code == 200:
            with open(f"{newspaper}/{filename}.pdf", 'wb') as f:
                f.write(response.content)
            with open('download_results.txt', 'a') as f:
                f.write(f"{newspaper}/{filename}.pdf was downloaded.\n")
            print(f"{newspaper}/{filename}.pdf was downloaded")
        elif response.status_code == 500:
            print('multiple files')
            number = 1
            loop = True
            try:
                os.mkdir(f'{newspaper}/{filename}')
            except FileExistsError:
                pass
            while loop:
                if f"{number}.pdf" not in os.listdir(f"{newspaper}/{filename}"):
                    site = f"https://www.pressarchive.cy/files/v2/publication_{code}_{number}/pdf"
                    print(site)
                    response = requests.get(url=site)
                    if response.status_code == 200:
                        with open(f'{newspaper}/{filename}/{number}.pdf','wb') as f:
                            f.write(response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{newspaper}/{filename}/{number}.pdf was downloaded\n")
                            print(f"{newspaper}/{filename}/{number}.pdf was downloaded")
                        number += 1
                    else:
                        loop = False
                else:
                    number += 1
        else:
            with open('download_results.txt', 'a') as f:
                f.write(f"{newspaper}/{filename} was not downloaded,it had response {response.status_code}\n")
            print(f"{newspaper}/{filename} was not downloaded,it had response {response.status_code}")


    # The following method will check all the newspapers
    def check_newspapers(self):
        for newspaper in self.newspaper_dictionary:
            self.check_newspaper(newspaper)

    # This method will print the names/codes of all the newspapers
    def print_newspaper_names(self):
        for newspaper in self.newspaper_dictionary:
            print(newspaper)

if __name__ == "__main__":
    cpio = CyprusPressInformationOffice()
    links = {'ΠΟΛΙΤΗΣ-31198': 'https://www.pressarchive.cy/s/en/item/31198?q=', 'ΣΗΜΕΡΙΝΗ (Η)-31199': 'https://www.pressarchive.cy/s/en/item/31199?q=', 'ΧΑΡΑΥΓΗ-31200': 'https://www.pressarchive.cy/s/en/item/31200?q=', 'ΑΛΗΘΕΙΑ-31201': 'https://www.pressarchive.cy/s/en/item/31201?q=', 'ΜΑΣΤΙΓΙΟΝ-31202': 'https://www.pressarchive.cy/s/en/item/31202?q=', 'ΗΧΩ ΤΗΣ ΚΥΠΡΟΥ-31204': 'https://www.pressarchive.cy/s/en/item/31204?q=', 'ΚΑΜΠΑΝΑ-31205': 'https://www.pressarchive.cy/s/en/item/31205?q=', 'ΜΑΧΗ-31209': 'https://www.pressarchive.cy/s/en/item/31209?q=', 'ΑΓΩΝ-64932': 'https://www.pressarchive.cy/s/en/item/64932?q=', 'ΑΝΕΞΑΡΤΗΤΟΣ-64933': 'https://www.pressarchive.cy/s/en/item/64933?q=', 'ΑΘΛΗΤΙΚΗ-64934': 'https://www.pressarchive.cy/s/en/item/64934?q=', 'ΕΡΓΑΤΗΣ-64936': 'https://www.pressarchive.cy/s/en/item/64936?q=', 'ΕΣΠΕΡΙΝΗ-64937': 'https://www.pressarchive.cy/s/en/item/64937?q=', 'ΕΘΝΟΣ (ΝΕΟΝ)-64938': 'https://www.pressarchive.cy/s/en/item/64938?q=', 'ΕΥΑΓΟΡΑΣ-64939': 'https://www.pressarchive.cy/s/en/item/64939?q=', 'ΦΩΝΗ ΤΗΣ ΚΥΠΡΟΥ (ΝΕΑ)-64941': 'https://www.pressarchive.cy/s/en/item/64941?q=', 'ΕΛΕΥΘΕΡΙΑ-64942': 'https://www.pressarchive.cy/s/en/item/64942?q=', 'ΓΝΩΜΗ-64943': 'https://www.pressarchive.cy/s/en/item/64943?q=', 'ΓΡΑΜΜΑΤΑ (ΤΑ)-64944': 'https://www.pressarchive.cy/s/en/item/64944?q=', 'ΚΥΠΡΙΑΚΟΣ ΤΥΠΟΣ-64945': 'https://www.pressarchive.cy/s/en/item/64945?q=', 'ΚΥΠΡΟΣ-64946': 'https://www.pressarchive.cy/s/en/item/64946?q=', 'ΛΑΪΚΟΝ ΒΗΜΑ-64947': 'https://www.pressarchive.cy/s/en/item/64947?q=', 'ΝΕΟΙ ΚΑΙΡΟΙ-64948': 'https://www.pressarchive.cy/s/en/item/64948?q=', 'ΠΑΦΟΣ-64949': 'https://www.pressarchive.cy/s/en/item/64949?q=', 'ΠΑΡΑΤΗΡΗΤΗΣ (Ο)-64950': 'https://www.pressarchive.cy/s/en/item/64950?q=', 'ΠΑΤΡΙΣ-64951': 'https://www.pressarchive.cy/s/en/item/64951?q=', 'ΦΙΛΑΘΛΟΣ-64952': 'https://www.pressarchive.cy/s/en/item/64952?q=', 'ΚΥΠΡΙΑΚΟΣ ΦΥΛΑΞ (ΝΕΟΣ)-64953': 'https://www.pressarchive.cy/s/en/item/64953?q=', 'ΠΡΩΙΝΗ-64954': 'https://www.pressarchive.cy/s/en/item/64954?q=', 'ΣΑΛΠΙΓΞ-64955': 'https://www.pressarchive.cy/s/en/item/64955?q=', 'ΣΤΑΣΙΝΟΣ-64956': 'https://www.pressarchive.cy/s/en/item/64956?q=', 'ΘΑΡΡΟΣ (ΤΟ)-64957': 'https://www.pressarchive.cy/s/en/item/64957?q=', 'CYPRUS TIMES (THE)-64958': 'https://www.pressarchive.cy/s/en/item/64958?q=', 'ΤΕΛΕΥΤΑΙΑ ΩΡΑ (Η)-64959': 'https://www.pressarchive.cy/s/en/item/64959?q=', 'ΧΡΟΝΟΣ-64960': 'https://www.pressarchive.cy/s/en/item/64960?q=', 'ΑΘΛΗΤΙΚΟ ΒΗΜΑ-1125363': 'https://www.pressarchive.cy/s/en/item/1125363?q=', 'ΒΡΑΔΥΝΗ (Η)-1125364': 'https://www.pressarchive.cy/s/en/item/1125364?q=', 'CMC WELFARE NEWS-1125365': 'https://www.pressarchive.cy/s/en/item/1125365?q=', 'CYPRUS PICTORIAL-1125366': 'https://www.pressarchive.cy/s/en/item/1125366?q=', 'ΔΙΑΒΟΛΟΣ (Ο)-1125367': 'https://www.pressarchive.cy/s/en/item/1125367?q=', 'CYPRUS REVIEW (ΠΕΡΙΟΔΙΚΟ)-1125368': 'https://www.pressarchive.cy/s/en/item/1125368?q=', 'ΔΕΙΛΙΝΗ (Η)-1125369': 'https://www.pressarchive.cy/s/en/item/1125369?q=', 'ΔΗΜΟΚΡΑΤΗΣ-1125370': 'https://www.pressarchive.cy/s/en/item/1125370?q=', 'ΔΗΜΙΟΥΡΓΙΑ-1125371': 'https://www.pressarchive.cy/s/en/item/1125371?q=', 'ΔΡΑΣΙΣ-1125372': 'https://www.pressarchive.cy/s/en/item/1125372?q=', 'ΕΙΔΗΣΕΙΣ-1125373': 'https://www.pressarchive.cy/s/en/item/1125373?q=', 'ΕΦΗΜΕΡΙΣ ΤΟΥ ΛΑΟΥ-1125374': 'https://www.pressarchive.cy/s/en/item/1125374?q=', 'ΕΦΗΜΕΡΙΣ-1125375': 'https://www.pressarchive.cy/s/en/item/1125375?q=', 'ΕΚΛΟΓΙΚΗ ΑΝΑΜΕΤΡΗΣΗ-1125376': 'https://www.pressarchive.cy/s/en/item/1125376?q=', 'ΕΚΠΑΙΔΕΥΤΙΚΟΣ (Ο)-1125377': 'https://www.pressarchive.cy/s/en/item/1125377?q=', 'ΕΚΚΛΗΣΙΑΣΤΙΚΟΝ ΒΗΜΑ-1125378': 'https://www.pressarchive.cy/s/en/item/1125378?q=', 'ΕΙΚΟΝΕΣ ΤΗΣ ΚΥΠΡΟΥ-1125379': 'https://www.pressarchive.cy/s/en/item/1125379?q=', 'ΕΚΚΛΗΣΙΑΣΤΙΚΗ ΖΩΗ-1125380': 'https://www.pressarchive.cy/s/en/item/1125380?q=', 'ΕΛΕΥΘΕΡΑ ΦΩΝΗ-1125381': 'https://www.pressarchive.cy/s/en/item/1125381?q=', 'ΕΛΕΥΘΕΡΟΣ ΛΑΟΣ-1125382': 'https://www.pressarchive.cy/s/en/item/1125382?q=', 'ΕΛΛΗΝΙΚΗ (Η)-1125383': 'https://www.pressarchive.cy/s/en/item/1125383?q=', 'ΕΛΕΥΘΕΡΩΤΗΣ (O)-1125384': 'https://www.pressarchive.cy/s/en/item/1125384?q=', 'ΕΛΕΥΘΕΡΟΣ ΤΥΠΟΣ-1125385': 'https://www.pressarchive.cy/s/en/item/1125385?q=', 'ΕΜΠΟΡΙΚΗ ΚΥΠΡΟΣ-1125386': 'https://www.pressarchive.cy/s/en/item/1125386?q=', 'ΕΜΠΟΡΙΚΗ-1125387': 'https://www.pressarchive.cy/s/en/item/1125387?q=', 'ΕΠΑΛΞΙΣ-1125388': 'https://www.pressarchive.cy/s/en/item/1125388?q=', 'ΕΡΓΑΤΙΚΟΣ ΑΓΩΝΑΣ-1125389': 'https://www.pressarchive.cy/s/en/item/1125389?q=', 'ΕΡΓΑΤΙΚΑ ΝΕΑ-1125390': 'https://www.pressarchive.cy/s/en/item/1125390?q=', 'ΕΜΠΟΡΙΚΗ (Η)-1125391': 'https://www.pressarchive.cy/s/en/item/1125391?q=', 'ΕΜΠΟΡΙΚΟΣ ΣΥΜΒΟΥΛΟΣ (Ο)-1125392': 'https://www.pressarchive.cy/s/en/item/1125392?q=', 'ΕΘΝΙΚΟΣ ΦΥΛΑΚΑΣ-1125393': 'https://www.pressarchive.cy/s/en/item/1125393?q=', 'ΕΘΝΙΚΗ ΝΕΟΛΑΙΑ-1125394': 'https://www.pressarchive.cy/s/en/item/1125394?q=', 'ΕΧΠΡΕΣ-1125395': 'https://www.pressarchive.cy/s/en/item/1125395?q=', 'ΕΞΟΡΜΗΣΗ-1125396': 'https://www.pressarchive.cy/s/en/item/1125396?q=', 'ΦΩΝΗ ΤΩΝ ΑΓΡΟΤΩΝ-1125397': 'https://www.pressarchive.cy/s/en/item/1125397?q=', 'ΦΑΚΟΣ (Ο)-1125398': 'https://www.pressarchive.cy/s/en/item/1125398?q=', 'ΗΧΩ ΤΩΝ ΕΛΛΗΝΩΝ-1125400': 'https://www.pressarchive.cy/s/en/item/1125400?q=', 'ΛΑΪΚΗ (Η)-1125401': 'https://www.pressarchive.cy/s/en/item/1125401?q=', 'ΚΥΠΡΙΑΚΗ ΕΠΙΘΕΩΡΗΣΙΣ-1125402': 'https://www.pressarchive.cy/s/en/item/1125402?q=', 'ΚΥΠΡΙΑΚΗ ΕΠΙΘΕΩΡΗΣΙΣ (ΠΕΡΙΟΔΙΚΟ)-1125403': 'https://www.pressarchive.cy/s/en/item/1125403?q=', 'ΚΑΘΗΜΕΡΙΝΑ ΦΥΛΛΑ-1125404': 'https://www.pressarchive.cy/s/en/item/1125404?q=', 'ΚΑΘΗΜΕΡΙΝΗ (Η)-1125405': 'https://www.pressarchive.cy/s/en/item/1125405?q=', 'ΚΕΡΥΝΕΙΑ-1125406': 'https://www.pressarchive.cy/s/en/item/1125406?q=', 'ΚΥΠΡΙΑΚΑ ΝΕΙΑΤΑ (ΤΑ)-1125301': 'https://www.pressarchive.cy/s/en/item/1125301?q=', 'ΚΥΠΡΙΑΚΗ ΑΝΑΠΤΥΞΙΣ-1125302': 'https://www.pressarchive.cy/s/en/item/1125302?q=', 'ΚΥΡΙΑΚΑΤΙΚΗ-1125303': 'https://www.pressarchive.cy/s/en/item/1125303?q=', 'ΚΥΠΡΙΑΚΗ-1125304': 'https://www.pressarchive.cy/s/en/item/1125304?q=', 'ΚΑΡΠΑΣΙΑ-1125305': 'https://www.pressarchive.cy/s/en/item/1125305?q=', 'ΚΟΣΜΟΣ-1125306': 'https://www.pressarchive.cy/s/en/item/1125306?q=', 'ΠΟΡΕΙΑ-1125307': 'https://www.pressarchive.cy/s/en/item/1125307?q=', 'ΠΡΩΪΑ-1125308': 'https://www.pressarchive.cy/s/en/item/1125308?q=', 'ΠΡΩΤΟΠΟΡΟΙ-1125309': 'https://www.pressarchive.cy/s/en/item/1125309?q=', 'ΠΥΡΣΟΣ-1125310': 'https://www.pressarchive.cy/s/en/item/1125310?q=', 'ΠΡΩΤΟΠΟΡΟΣ-1125311': 'https://www.pressarchive.cy/s/en/item/1125311?q=', 'ΠΑΡΑΣΚΗΝΙΟ (ΤΟ)-1125312': 'https://www.pressarchive.cy/s/en/item/1125312?q=', 'ΠΡΩΤΕΥΟΥΣΑ-1125313': 'https://www.pressarchive.cy/s/en/item/1125313?q=', 'ΠΥΞ ΛΑΞ-1125314': 'https://www.pressarchive.cy/s/en/item/1125314?q=', 'ΡΑΓΙΑΣ (Ο)-1125315': 'https://www.pressarchive.cy/s/en/item/1125315?q=', 'ΡΙΖΟΣΠΑΣΤΙΚΟ ΒΗΜΑ-1125316': 'https://www.pressarchive.cy/s/en/item/1125316?q=', 'ΡΟΥΚΑΝΟΣ-1125317': 'https://www.pressarchive.cy/s/en/item/1125317?q=', 'ΣΗΜΑΙΑ ΤΗΣ ΚΥΠΡΟΥ-1125318': 'https://www.pressarchive.cy/s/en/item/1125318?q=', 'ΣΑΛΠΙΞ-1125319': 'https://www.pressarchive.cy/s/en/item/1125319?q=', 'ΣΥΝΕΙΔΗΣΗ-1125320': 'https://www.pressarchive.cy/s/en/item/1125320?q=', 'ΣΥΝΑΓΕΡΜΟΣ-1125321': 'https://www.pressarchive.cy/s/en/item/1125321?q=', 'ΣΠΟΡΤ-1125322': 'https://www.pressarchive.cy/s/en/item/1125322?q=', 'ΣΠΟΡΤΣ ΤΑΪΜΣ-1125323': 'https://www.pressarchive.cy/s/en/item/1125323?q=', 'ΤΑΧΥΔΡΟΜΟΣ-1125324': 'https://www.pressarchive.cy/s/en/item/1125324?q=', 'CYPRUS SHIPPING NEWS AND COMMERCIAL REGISTER (THE)-1125325': 'https://www.pressarchive.cy/s/en/item/1125325?q=', 'CYPRUS WEEKLY (THE)-1125326': 'https://www.pressarchive.cy/s/en/item/1125326?q=', 'CYPRIOT (THE)-1125327': 'https://www.pressarchive.cy/s/en/item/1125327?q=', 'ΤΗΛΕΓΡΑΦΟΣ (Ο)-1125328': 'https://www.pressarchive.cy/s/en/item/1125328?q=', 'ΤΗΛΕΡΑΜΑ-1125329': 'https://www.pressarchive.cy/s/en/item/1125329?q=', 'ΝΕΑ (ΤΑ)-1125330': 'https://www.pressarchive.cy/s/en/item/1125330?q=', 'SPORTS TIMES-1125331': 'https://www.pressarchive.cy/s/en/item/1125331?q=', 'ΦΩΝΗ ΤΟΥ ΚΥΠΡΙΑΚΟΥ ΛΑΟΥ (Η)-1125332': 'https://www.pressarchive.cy/s/en/item/1125332?q=', 'ΚΥΡΙΑΚΑΤΙΚΟΣ ΤΥΠΟΣ-1125333': 'https://www.pressarchive.cy/s/en/item/1125333?q=', 'ΚΗΡΥΞ-1125334': 'https://www.pressarchive.cy/s/en/item/1125334?q=', 'ΚΤΗΜΑΤΙΚΗ (Η)-1125335': 'https://www.pressarchive.cy/s/en/item/1125335?q=', 'ΛΑΪΚΗ ΗΧΩ-1125336': 'https://www.pressarchive.cy/s/en/item/1125336?q=', 'ΜΙΚΡΟΥΛΑ-1125338': 'https://www.pressarchive.cy/s/en/item/1125338?q=', 'ΜΕΣΗΜΒΡΙΝΗ-1125339': 'https://www.pressarchive.cy/s/en/item/1125339?q=', 'ΜΑΘΗΤΙΚΗ (Η)-1125340': 'https://www.pressarchive.cy/s/en/item/1125340?q=', 'ΝΕΟΣ ΔΗΜΟΚΡΑΤΗΣ-1125341': 'https://www.pressarchive.cy/s/en/item/1125341?q=', 'ΝΕΑ ΕΦΗΜΕΡΙΣ ΤΗΣ ΛΕΥΚΩΣΙΑΣ (Η)-1125342': 'https://www.pressarchive.cy/s/en/item/1125342?q=', 'ΝΕΑ ΓΕΝΙΑ-1125343': 'https://www.pressarchive.cy/s/en/item/1125343?q=', 'ΝΙΚΗ (Η)-1125344': 'https://www.pressarchive.cy/s/en/item/1125344?q=', 'ΝΕΟΝ ΚΙΤΙΟΝ-1125345': 'https://www.pressarchive.cy/s/en/item/1125345?q=', 'ΝΕΟΣ ΚΟΣΜΟΣ-1125346': 'https://www.pressarchive.cy/s/en/item/1125346?q=', 'ΝΕΑ ΛΑΪΚΗ-1125347': 'https://www.pressarchive.cy/s/en/item/1125347?q=', 'ΝΕΑ ΜΙΚΡΟΥΛΛΑ-1125348': 'https://www.pressarchive.cy/s/en/item/1125348?q=', 'ΝΕΑ ΠΟΛΙΤΙΚΗ ΕΠΙΘΕΩΡΗΣΙΣ-1125349': 'https://www.pressarchive.cy/s/en/item/1125349?q=', 'ΝΕΑ ΠΟΛΙΤΕΙΑ-1125350': 'https://www.pressarchive.cy/s/en/item/1125350?q=', 'ΝΕΑ ΠΝΟΗ-1125351': 'https://www.pressarchive.cy/s/en/item/1125351?q=', 'ΔΕΛΤΙΟΝ ΟΕΛΜΕΚ-1125352': 'https://www.pressarchive.cy/s/en/item/1125352?q=', 'ΠΟΛΙΤΙΚΗ ΕΠΙΘΕΩΡΗΣΙΣ (Η)-1125353': 'https://www.pressarchive.cy/s/en/item/1125353?q=', 'ΠΟΛΙΤΕΙΑ-1125354': 'https://www.pressarchive.cy/s/en/item/1125354?q=', 'ΠΑΝΑΓΡΟΤΙΚΗ-1125355': 'https://www.pressarchive.cy/s/en/item/1125355?q=', 'ΑΔΕΣΜΕΥΤΗ-1125356': 'https://www.pressarchive.cy/s/en/item/1125356?q=', 'ΑΓΩΝΙΣΤΙΚΗ ΠΟΡΕΙΑ-1125357': 'https://www.pressarchive.cy/s/en/item/1125357?q=', 'ΑΙΩΝ-1125358': 'https://www.pressarchive.cy/s/en/item/1125358?q=', 'ΑΔΟΥΛΩΤΗ ΚΕΡΥΝΕΙΑ (Η)-1125359': 'https://www.pressarchive.cy/s/en/item/1125359?q=', 'ΑΚΡΟΠΟΛΙΣ-1125360': 'https://www.pressarchive.cy/s/en/item/1125360?q=', 'ΑΝΕΞΑΡΤΗΤΟΣ-1125361': 'https://www.pressarchive.cy/s/en/item/1125361?q=', 'ΑΠΟΣΤΡΑΤΟΣ-1125362': 'https://www.pressarchive.cy/s/en/item/1125362?q=', 'ΑΛΗΘΕΙΑ-1589724': 'https://www.pressarchive.cy/s/en/item/1589724?q=', 'ΝΕΑ ΕΣΠΕΡΙΝΗ-1589726': 'https://www.pressarchive.cy/s/en/item/1589726?q=', 'ΕΣΠΕΡΙΝΗ-1589727': 'https://www.pressarchive.cy/s/en/item/1589727?q=', 'ΕΛΕΥΘΕΡΟΣ ΛΑΟΣ-1589728': 'https://www.pressarchive.cy/s/en/item/1589728?q=', 'COMMERCIAL CYPRUS-1589729': 'https://www.pressarchive.cy/s/en/item/1589729?q=', 'ΕΦΗΜΕΡΙΣ ΤΟΥ ΛΑΟΥ-1589730': 'https://www.pressarchive.cy/s/en/item/1589730?q=', 'ΚΥΠΡΙΑΚΗ (Η)-1589731': 'https://www.pressarchive.cy/s/en/item/1589731?q=', 'ΜΑΧΗ Free Press-1589732': 'https://www.pressarchive.cy/s/en/item/1589732?q=', 'ΠΑΤΡΙΣ-1589733': 'https://www.pressarchive.cy/s/en/item/1589733?q=', 'ΠΑΤΡΙΣ-1589734': 'https://www.pressarchive.cy/s/en/item/1589734?q=', 'ΠΟΛΙΤΕΙΑ-1589735': 'https://www.pressarchive.cy/s/en/item/1589735?q=', 'ΠΡΩΙΝΗ (ΝΕΑ)-1589736': 'https://www.pressarchive.cy/s/en/item/1589736?q=', 'ΑΓΩΝ-1589737': 'https://www.pressarchive.cy/s/en/item/1589737?q=', 'ΑΓΩΝ (Ο)-1589738': 'https://www.pressarchive.cy/s/en/item/1589738?q=', 'ΝΕΑ (ΤΑ)-1589739': 'https://www.pressarchive.cy/s/en/item/1589739?q=', 'ΝΕΑ (ΤΑ)-1589740': 'https://www.pressarchive.cy/s/en/item/1589740?q=', 'ΕΘΝΟΣ-1589741': 'https://www.pressarchive.cy/s/en/item/1589741?q=', 'ΚΥΠΡΟΣ-1589743': 'https://www.pressarchive.cy/s/en/item/1589743?q=', 'ΚΥΠΡΟΣ-1589745': 'https://www.pressarchive.cy/s/en/item/1589745?q=', 'ΚΥΠΡΟΣ-1589746': 'https://www.pressarchive.cy/s/en/item/1589746?q=', 'ΚΥΠΡΟΣ-1589747': 'https://www.pressarchive.cy/s/en/item/1589747?q=', 'ΚΥΠΡΙΟΣ-1589749': 'https://www.pressarchive.cy/s/en/item/1589749?q=', 'CYPRUS MAIL-64935': 'https://www.pressarchive.cy/s/en/item/64935?q=', 'TIMES OF CYPRUS-1770146': 'https://www.pressarchive.cy/s/en/item/1770146?q='}
    for paper in links:
        cpio.check_newspaper(paper)
