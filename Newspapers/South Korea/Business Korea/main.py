#Business Korea is a business magazine in South Korea


import requests,lxml,time
from bs4 import BeautifulSoup
from selenium import webdriver

class BusinessKorea:
    def __init__(self):
        self.special_character = "호"
        self.magazine_dictionary: dict = self.return_dictionary()
        print(self.magazine_dictionary)
        self.minimum = 336
        self.maximum = self.return_max()
        self.not_possible = self.not_possible

        self.missing = self.return_missing()
        self.start_driver()

    #The magazines that cannot be downloaded at all
    def not_possible(self)->list:
        return [383,384,391]



    #This method starts the selenium webdriver to find the new urls that gets redirected
    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url="https://www.businesskorea.co.kr/index2.html")

    #This method will return a dictionary with the number being the key and the date being the value
    def return_dictionary(self)->dict:
        page = "https://www.businesskorea.co.kr/pdf/list.html"
        soup = BeautifulSoup(requests.get(url=page).text,"lxml")
        options = [option.text.strip(self.special_character) for option in soup.find_all("option")]

        options = options[1:]
        dictionary = {}

        for option in options:
            items = option.split()
            count = int(items[0])
            date = items[1].strip("(").strip(")")

            dictionary[count] = date
        dictionary[411] = "2023-04-01"
        return dictionary

    #This method will find the largest magazine number
    def return_max(self):
        maximum = self.minimum
        for key in self.magazine_dictionary:
            if key > maximum:
                maximum = key

        return maximum

    #This method will return a list of missing magazine numbers
    def return_missing(self)->list:
        missing = []
        for i in range(self.minimum,self.maximum+1):
            if i not in self.magazine_dictionary:
                missing.append(i)

        return missing


    #This method will download a specific numbered magazine for Business Korea
    def download(self,number):
        if self.minimum < number < self.maximum:
            #This will check whether the number is missing
            if number not in self.missing :
                date = self.magazine_dictionary[number]
                name = f"{number}-{date}"
                page = f"https://www.businesskorea.co.kr/pdf/list.html?category=&hosu={name}"

                print(page)
                soup = BeautifulSoup(requests.get(url=page).text,"lxml")

                pdf_links= [link["href"] for link in soup.find_all("a",href=True) if "check.php" in link["href"]]

                print(pdf_links)
                page = "https://www.businesskorea.co.kr/pdf/"

                for pdf_link in pdf_links[0:1]:
                    page += pdf_link

                print(page)



                self.driver.get(page)
                time.sleep(2)
                current_page = self.driver.current_url
                print(current_page)

                response = requests.get(current_page)


                if response.status_code == 200:
                    with open(f"{name}.pdf","wb") as f:
                        f.write(response.content)
                    with open("download_results.txt","a") as f:
                        f.write(f"{name} was downloaded\n")
                    print(f"{name} was downloaded\n")
                else:
                    with open("download_results.txt","a") as f:
                        f.write(f"{name} was not downloaded, it had response status code {response.status_code}\n")
                    print(f"{name} was not downloaded, it had response status code {response.status_code}\n")


    #This method will download all the magazines from n1 to n2
    #If n1 is 100 and n2 is 105,
    #It will download: 100,101,102,103,104,105
    def download_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.download(i)


    #This method will download the entire archive on the Business Korea archive
    def download_all(self):
        self.download_n1_n2(n1=self.minimum,n2=self.maximum)

    #This method will download the latest magazine of Business Korea
    def download_latest(self):
        self.download(number=self.maximum)

if __name__ == "__main__":
    bk = BusinessKorea()
    print(bk.maximum)
    bk.download(411)
