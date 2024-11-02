import requests, lxml, time, datetime, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Lego.com lego sets pdf web scraper
class LegoInstructions:
    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.enter_site()

        self.year_amount = {}
        self.year_clicks = {}
        self.get_years()
        self.year_amount = dict(sorted(self.year_amount.items()))
        self.themes = {}
        self.theme_clicks = {}
        self.get_themes()

    def enter_site(self):
        # code to click on to pass by notifications et cetera
        self.driver.get(url="https://www.lego.com/en-us/service/buildinginstructions/")
        time.sleep(3)
        continue_button = self.driver.find_element(By.ID, "age-gate-grown-up-cta")
        continue_button.click()
        time.sleep(5)
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        dismiss_button = [button for button in buttons if button.text == "Dismiss"][0]
        dismiss_button.click()

    def get_pdf_names(self):
        try:
            with open("pdf_files.txt", "r") as f:
                pdfs = f.readlines()
                pdfs = [pdf.replace("\n", "") for pdf in pdfs]
        except FileNotFoundError:
            with open("pdf_files.txt", "w") as f:
                f.write("")
                pdfs = []
        self.pdfs = pdfs

    def get_years(self):
        html_content = self.driver.page_source
        lego_soup = BeautifulSoup(html_content, "lxml")
        self.driver.execute_script("window.scrollBy(0, 1100);")
        select_tags = \
        [select.find_all("option") for select in lego_soup.find_all("select", class_="c-form-item__control") if
         select["id"] == "filter-year"][0]
        options = [select.text.strip() for select in select_tags]

        for option in options:
            result = option.split(" ")
            year = int(result[0])
            amount = int(result[1].strip("(").strip(")"))
            self.year_amount[year] = amount
            click_amount = amount
            if click_amount <= 12:
                self.year_clicks[year] = 0
            elif click_amount % 12 == 0:
                self.year_clicks[year] = (click_amount - 12) // 12
            else:
                self.year_clicks[year] = (click_amount - 12) // 12 + 1

    # This
    def get_themes(self):
        html_content = self.driver.page_source
        lego_soup = BeautifulSoup(html_content, "lxml")
        self.driver.execute_script("window.scrollBy(0, 1600);")
        select_tags = \
        [select.find_all("option") for select in lego_soup.find_all("select", class_="c-form-item__control") if
         select["id"] == "filter-theme"][0]
        values = [select["value"] for select in select_tags]
        options = [select.text.strip() for select in select_tags]

        self.themes = {options[i]: values[i] for i in range(len(options))}

        for option in options:
            option_amount = int(option.split("(")[-1].strip(")"))
            if option_amount <= 12:
                self.theme_clicks[option] = 0
            elif option_amount % 12 == 0:
                self.theme_clicks[option] = (option_amount - 12) // 12
            else:
                self.theme_clicks[option] = (option_amount - 12) // 12 + 1

    def show_themes(self):
        print([key for key, value in self.theme_clicks.items()])

    def download_theme(self, theme: str):
        if theme in self.theme_clicks:
            theme_url = self.themes[theme]
            theme_site = f"https://www.lego.com/en-us/service/buildinginstructions/search?q=&theme={theme_url}&sort=setnumber"
            self.driver.get(url=theme_site)
            click_amount = self.theme_clicks[theme]
            time.sleep(5)

            for i in range(click_amount):
                self.driver.execute_script("window.scrollBy(0, 1600);")
                load_button = \
                [button for button in self.driver.find_elements(By.TAG_NAME, "button") if "Load more" in button.text][0]
                load_button.click()
                time.sleep(2)

            html_content = self.driver.page_source
            year_soup = BeautifulSoup(html_content, "lxml")
            lego_sets = sorted(list(
                set([f"https://www.lego.com{anchor_tag['href']}" for anchor_tag in year_soup.find_all("a", href=True) if
                     "View Instructions" in anchor_tag.text])))
            os.makedirs(theme)
            for lego_set in lego_sets:

                self.driver.get(url=lego_set)
                time.sleep(1.5)
                self.driver.execute_script("window.scrollBy(0, 1600);")
                set_id = lego_set.split("/")[-1]
                set_html = self.driver.page_source
                set_soup = BeautifulSoup(set_html, "lxml")
                pdf_files = [f"{pdf['href']}" for pdf in set_soup.find_all("a", href=True) if
                             "pdf" in pdf["href"] and "LEGO_Modern_Slavery_Transparency_Statement_2023_FINAL.pdf" not in
                             pdf["href"]]
                os.makedirs(f"{theme}/{set_id}")

                for pdf in pdf_files:
                    response = requests.get(url=pdf)
                    pdf_name = pdf.split("/")[-1]
                    if response.status_code == 200:

                        with open(f"{theme}/{set_id}/{pdf_name}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{set_id} {pdf_name} was downloaded\n")
                        print(f"{set_id} {pdf_name} was downloaded\n")
                        with open("pdf_files.txt", "a") as f:
                            f.write(f"{pdf_name}\n")

                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

                        print(
                            f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

    def download_themes(self):
        for theme in self.themes:
            theme_url = self.themes[theme]
            theme_site = f"https://www.lego.com/en-us/service/buildinginstructions/search?q=&theme={theme_url}&sort=setnumber"
            self.driver.get(url=theme_site)
            click_amount = self.theme_clicks[theme]
            time.sleep(5)

            for i in range(click_amount):
                self.driver.execute_script("window.scrollBy(0, 1600);")
                load_button = \
                [button for button in self.driver.find_elements(By.TAG_NAME, "button") if "Load more" in button.text][0]
                load_button.click()
                time.sleep(2)

            html_content = self.driver.page_source
            year_soup = BeautifulSoup(html_content, "lxml")
            lego_sets = sorted(list(
                set([f"https://www.lego.com{anchor_tag['href']}" for anchor_tag in year_soup.find_all("a", href=True) if
                     "View Instructions" in anchor_tag.text])))
            os.makedirs(theme)
            for lego_set in lego_sets:

                self.driver.get(url=lego_set)
                time.sleep(1.5)
                self.driver.execute_script("window.scrollBy(0, 1600);")
                set_id = lego_set.split("/")[-1]
                set_html = self.driver.page_source
                set_soup = BeautifulSoup(set_html, "lxml")
                pdf_files = [f"{pdf['href']}" for pdf in set_soup.find_all("a", href=True) if
                             "pdf" in pdf["href"] and "LEGO_Modern_Slavery_Transparency_Statement_2023_FINAL.pdf" not in
                             pdf["href"]]
                os.makedirs(f"{theme}/{set_id}")

                for pdf in pdf_files:

                    response = requests.get(url=pdf)
                    pdf_name = pdf.split("/")[-1]

                    if response.status_code == 200:

                        with open(f"{theme}/{set_id}/{pdf_name}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{set_id} {pdf_name} was downloaded\n")
                        print(f"{set_id} {pdf_name} was downloaded\n")
                        with open("pdf_files.txt", "a") as f:
                            f.write(f"{pdf_name}\n")
                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

                        print(
                            f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

    def download_year(self, year: int):
        # Enter any year from 1996 to the current year that we are in
        current_year = datetime.datetime.now().year

        if int(year) >= 1996 and int(year) <= current_year:
            website = f"https://www.lego.com/en-us/service/buildinginstructions/search?q=&year={year}&sort=setnumber"
            self.driver.get(website)
            click_amount = self.year_clicks[year]
            time.sleep(5)

            for i in range(click_amount):
                self.driver.execute_script("window.scrollBy(0, 1100);")
                load_button = \
                [button for button in self.driver.find_elements(By.TAG_NAME, "button") if "Load more" in button.text][0]
                load_button.click()
                time.sleep(2)

            html_content = self.driver.page_source
            year_soup = BeautifulSoup(html_content, "lxml")
            lego_sets = sorted(list(
                set([f"https://www.lego.com{anchor_tag['href']}" for anchor_tag in year_soup.find_all("a", href=True) if
                     "View Instructions" in anchor_tag.text])))
            os.makedirs(str(year))

            for lego_set in lego_sets:

                self.driver.get(url=lego_set)
                time.sleep(1.5)
                self.driver.execute_script("window.scrollBy(0, 1100);")
                set_id = lego_set.split("/")[-1]
                set_html = self.driver.page_source
                set_soup = BeautifulSoup(set_html, "lxml")
                pdf_files = [f"{pdf['href']}" for pdf in set_soup.find_all("a", href=True) if
                             "pdf" in pdf["href"] and "LEGO_Modern_Slavery_Transparency_Statement_2023_FINAL.pdf" not in
                             pdf["href"]]
                os.makedirs(f"{year}/{set_id}")

                for pdf in pdf_files:

                    response = requests.get(url=pdf)
                    pdf_name = pdf.split("/")[-1]

                    if response.status_code == 200:

                        with open(f"{year}/{set_id}/{pdf_name}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{set_id} {pdf_name} was downloaded\n")
                        print(f"{set_id} {pdf_name} was downloaded\n")
                        with open("pdf_files.txt", "a") as f:
                            f.write(f"{pdf_name}\n")

                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

                        print(
                            f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

    def download_years(self):
        for year in self.year_amount:
            website = f"https://www.lego.com/en-us/service/buildinginstructions/search?q=&year={year}&sort=setnumber"
            self.driver.get(website)
            click_amount = self.year_clicks[year]
            time.sleep(5)

            for i in range(click_amount):
                self.driver.execute_script("window.scrollBy(0, 1600);")
                load_button = \
                [button for button in self.driver.find_elements(By.TAG_NAME, "button") if "Load more" in button.text][0]
                load_button.click()
                time.sleep(2)

            html_content = self.driver.page_source
            year_soup = BeautifulSoup(html_content, "lxml")
            lego_sets = sorted(list(
                set([f"https://www.lego.com{anchor_tag['href']}" for anchor_tag in year_soup.find_all("a", href=True) if
                     "View Instructions" in anchor_tag.text])))
            os.makedirs(str(year))

            for lego_set in lego_sets:

                self.driver.get(url=lego_set)
                time.sleep(1.5)
                self.driver.execute_script("window.scrollBy(0, 1100);")
                set_id = lego_set.split("/")[-1]
                set_html = self.driver.page_source
                set_soup = BeautifulSoup(set_html, "lxml")
                pdf_files = [f"{pdf['href']}" for pdf in set_soup.find_all("a", href=True) if
                             "pdf" in pdf["href"] and "LEGO_Modern_Slavery_Transparency_Statement_2023_FINAL.pdf" not in
                             pdf["href"]]
                os.makedirs(f"{year}/{set_id}")

                for pdf in pdf_files:

                    response = requests.get(url=pdf)
                    pdf_name = pdf.split("/")[-1]

                    if response.status_code == 200:

                        with open(f"{year}/{set_id}/{pdf_name}", "wb") as f:
                            f.write(response.content)
                        with open("download_results.txt", "a") as f:
                            f.write(f"{set_id} {pdf_name} was downloaded\n")
                        print(f"{set_id} {pdf_name} was downloaded\n")
                        with open("pdf_files.txt", "a") as f:
                            f.write(f"{pdf_name}\n")

                    else:
                        with open("download_results.txt", "a") as f:
                            f.write(
                                f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

                        print(
                            f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

    def update_year(self,year:int):
        self.get_pdf_names()
        if year in self.year_amount:
            website = f"https://www.lego.com/en-us/service/buildinginstructions/search?q=&year={year}&sort=setnumber"
            self.driver.get(website)
            click_amount = self.year_clicks[year]
            time.sleep(5)

            for i in range(click_amount):
                self.driver.execute_script("window.scrollBy(0, 1600);")
                load_button = \
                    [button for button in self.driver.find_elements(By.TAG_NAME, "button") if
                     "Load more" in button.text][0]
                load_button.click()
                time.sleep(2)

            html_content = self.driver.page_source
            year_soup = BeautifulSoup(html_content, "lxml")
            lego_sets = sorted(list(
                set([f"https://www.lego.com{anchor_tag['href']}" for anchor_tag in year_soup.find_all("a", href=True) if
                     "View Instructions" in anchor_tag.text])))
            try:
                os.makedirs(str(year))
            except FileExistsError:
                pass

            for lego_set in lego_sets:
                self.driver.get(url=lego_set)
                time.sleep(1.5)
                self.driver.execute_script("window.scrollBy(0, 1100);")
                set_id = lego_set.split("/")[-1]
                set_html = self.driver.page_source
                set_soup = BeautifulSoup(set_html, "lxml")
                pdf_files = [f"{pdf['href']}" for pdf in set_soup.find_all("a", href=True) if
                             "pdf" in pdf["href"] and "LEGO_Modern_Slavery_Transparency_Statement_2023_FINAL.pdf" not in
                             pdf["href"]]
                try:
                    os.makedirs(f"{year}/{set_id}")
                except FileExistsError:
                    pass

                for pdf in pdf_files:
                    response = requests.get(url=pdf)
                    pdf_name = pdf.split("/")[-1]

                    if pdf_name not in self.pdfs:
                        if response.status_code == 200:
                            with open(f"{year}/{set_id}/{pdf_name}", "wb") as f:
                                f.write(response.content)
                            with open("download_results.txt", "a") as f:
                                f.write(f"{set_id} {pdf_name} was downloaded\n")
                            print(f"{set_id} {pdf_name} was downloaded\n")
                            with open('pdf_files.txt', "a") as f:
                                f.write(f"{pdf_name}\n")

                        else:
                            with open("download_results.txt", "a") as f:
                                f.write(
                                    f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")

                            print(
                                f"{set_id} {pdf_name} was not downloaded, it had response status code {response.status_code}\n")
                    else:
                        print("This pdf has already been downloaded")

    def update_range(self,year1:int,year2:int):
        self.get_pdf_names()
        if year1 > year2:
            c = year2
            year2 = year1
            year1 = c

        for year in range(year1,year2+1):
            self.update_year(year)

    def update_all(self):
        self.get_pdf_names()
        for year in self.year_amount:
            self.update_year(year)



if __name__ == "__main__":
    li = LegoInstructions()

    # li.download_theme('LEGOLAND (5)')

    # li.update_all()
    # will download all the pdfs that might have been added to the lego.com website

    # li.update_year(year=2024)
    # will download all the pdfs that might have been added to a specific year

    # li.update_range(2000,2005)
    # will update all the pdfs from 2000 to 2005

    # li.update_all()
    # will update the entire archive

    # The following method will download a specific year between 1996 and the current year that we are in
    # the year input has to be an integer between 1996 to the year that we are in
    # li.download_year(year=1996)
    # li.download_year(year=2010)

    # This method will download all the years from 1996 to the current year that we are in and the lego sets will be in their respective years folder
    # The method takes no input
    # li.download_years()

    # The following method will download all the themes and the lego sets will be in their respective themes folder
    # The method takes no input
    # li.download_themes()

    # This method will show all the themes that you can choose from to download
    # This method is really helpful for the li.download_theme(), you can copy and paste as it is for the input it needs to download the exact theme
    # The method takes no input
    # li.show_themes()
    # Example output for 28th June 2024:
    """['LEGOLAND (5)', 'LEGO® (150)', 'LEGO® Adventurers (47)', 'LEGO® Agents (13)',
     'LEGO® Alien Conquest (7)', 'LEGO® Alpha Team (25)', 'LEGO® Animal Crossing™ (6)',
     'LEGO® Aqua Raiders (6)', 'LEGO® Aquazone (15)', 'LEGO® Architecture (54)', 'LEGO® Arctic (8)',
     'LEGO® Art (18)', 'LEGO® Atlantis (20)', 'LEGO® Avatar The Last Airbender (2)', 'LEGO® Avatar™ (9)',
     'LEGO® BATMAN™ (22)', 'LEGO® BIONICLE (259)', 'LEGO® BOOST (1)', 'LEGO® Belville (41)',
     'LEGO® Ben 10: Alien Force™ (6)', 'LEGO® Botanical Collection (18)', 'LEGO® BrickLink (10)',
     'LEGO® Brickheadz (144)', 'LEGO® Brickmaster (2)', 'LEGO® CHIMA™ (87)', 'LEGO® CLIKITS (25)',
     'LEGO® CREATOR Expert (76)', 'LEGO® Cars™ (32)', 'LEGO® Castle (78)', 'LEGO® Chinese Festivals (13)',
     'LEGO® City (743)', 'LEGO® Classic (135)', 'LEGO® Creator (252)', 'LEGO® DC (87)', 'LEGO® DINO (17)',
     'LEGO® DOTS (42)', 'LEGO® DREAMZzz™ (24)', 'LEGO® DUPLO® (349)', 'LEGO® Dimensions (65)', 'LEGO® Discovery (6)',
     'LEGO® Disney™ (156)', 'LEGO® Divers (8)', 'LEGO® Elves (33)', 'LEGO® Exo-Force (31)', 'LEGO® Ferrari™ (16)',
     'LEGO® Friends (405)', 'LEGO® Friends (108)', "LEGO® Gabby's Dollhouse (7)", 'LEGO® Galaxy Squad (10)',
     'LEGO® Games (37)', 'LEGO® Ghostbusters™ (2)', 'LEGO® HERO Factory (86)', 'LEGO® Harry Potter™ (133)',
     'LEGO® Hidden Side (19)', 'LEGO® Icons (49)', 'LEGO® Ideas (59)', 'LEGO® Indiana Jones™ (19)', 'LEGO® Juniors (55)',
     'LEGO® Jurassic World™ (50)', 'LEGO® Knights Kingdom (44)', 'LEGO® MINDSTORMS® (7)', 'LEGO® MINECRAFT (106)',
     'LEGO® Marvel™ (231)', 'LEGO® Minifigures (36)', 'LEGO® Minions (10)', 'LEGO® Mixels (81)', 'LEGO® Monkie Kid™ (50)',
     'LEGO® Monster Fighters (9)', 'LEGO® NEXO KNIGHTS (55)', 'LEGO® NINJAGO® (309)', 'LEGO® Ninja Turtles™ (11)',
     'LEGO® Overwatch® (8)', 'LEGO® Paradisa (4)', "LEGO® Pharaoh's Quest (6)", 'LEGO® Pirates (26)', 'LEGO® Pirates of the Caribbean™ (10)',
     'LEGO® Power Miners (16)', 'LEGO® Prince of Persia™ (5)', 'LEGO® Racers (184)', 'LEGO® Res-Q (6)', 'LEGO® RoboRiders (11)',
     'LEGO® Rock Raiders (6)', 'LEGO® Scala (17)', 'LEGO® Scooby-Doo (5)', 'LEGO® Sonic the Hedgehog™ (9)',
     'LEGO® Space (70)', 'LEGO® Speed Champions (72)', 'LEGO® Spider-Man™ (13)', 'LEGO® SpongeBob™ (14)',
     'LEGO® Sports (53)', 'LEGO® Star Wars™ (635)', 'LEGO® Stranger Things (1)', 'LEGO® Super Mario™ (81)',
     'LEGO® Technic (309)', 'LEGO® The Angry Birds™ Movie (6)', 'LEGO® The Batman Movie (25)',
     'LEGO® The Lord of the Rings™ (26)', 'LEGO® The Powerpuff Girls™ (2)', 'LEGO® The Simpsons™ (2)',
     'LEGO® Time Cruisers (6)', 'LEGO® Toy Story 4 (17)', 'LEGO® Trolls (8)', 'LEGO® Ultra Agents (14)',
     'LEGO® Unikitty™ (8)', 'LEGO® Vikings (7)', 'LEGO® Wild West (12)', 'LEGO® Znap (9)', 'LEGO®\xa0The Lone Ranger™ (6)',
     'THE LEGO® MOVIE 2™ (46)', 'THE LEGO® NINJAGO® MOVIE™ (20)', 'VIDIYO (15)']"""

    # li.download_theme(theme="THE LEGO® MOVIE 2™ (46)") is a way to use the method

    # This method will download a specific theme
    # Example usages of the method:
    # li.download_theme(theme='LEGO®\xa0The Lone Ranger™ (6)')
    # li.download_theme(theme='LEGO® Prince of Persia™ (5)')

    # The other methods in the class are for the initiation of the class and they should not be used after constructing the class
