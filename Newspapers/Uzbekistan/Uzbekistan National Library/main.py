#Webscraping the Uzbekistan National Library
#The main page is http://press.natlib.uz/en


import requests,lxml,json,os
from bs4 import BeautifulSoup


class UzbekistanNationalLibrary:
    def __init__(self):
        self.main_page = "http://press.natlib.uz/en/"
        self.minimum = 5
        self.maximum = self.find_latest()
        self.newspapers = self.return_newspapers()

    # This method will find all the newspapers
    def return_newspapers(self) -> dict:
        try:
            with open("newspapers.json", "r") as f:
                newspapers: dict = json.load(f)
                newspapers = list(newspapers.keys())
        except FileNotFoundError:
            with open("newspapers.json", "w") as f:
                json.dump({},f)
            newspapers = {}

        return newspapers

    #This method will show all the newspapers
    def show_newspapers(self):
        print(self.newspapers)

    #This method will find the latest number on the main webpage
    def find_latest(self)->int:
        soup = BeautifulSoup(requests.get(url=self.main_page).text, 'lxml')
        links = [int(f'{link["href"]}'.strip("/en/editions/")) for link in soup.find_all("a", href=True) if "/en/editions/" in link["href"]]
        return max(links)

    #This will find all the links and add to the json data
    def find_all(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2+1):
            try:
                with open("results.json", "r") as data:
                    results = json.load(data)
            except FileNotFoundError:
                with open("results.json", "w") as data:
                    results = {}
                    json.dump({}, data)

            try:
                with open("newspapers.json", "r") as data:
                    newspapers = json.load(data)
            except FileNotFoundError:
                with open("newspapers.json", "w") as data:
                    newspapers = {}
                    json.dump({}, data)


            page = f"http://press.natlib.uz/en/editions/{i}"
            soup = BeautifulSoup(requests.get(url=page).text,"lxml")
            links = [link.text for link in soup.find_all("a",href=True) if "/en/editions" in link["href"]]
            spans = soup.find_all("span")
            spans = [span.text for span in spans if "Download" == span.text]
            print(len(spans),i)

            # if there are no spans it means it cannot be downloaded, or it does not exist
            if len(spans) == 1:
                newspaper_name = links[-1]
                if newspaper_name in newspapers:
                    newspapers[newspaper_name] += 1
                else:
                    newspapers[newspaper_name] = 1
                count = newspapers[newspaper_name]

                with open("results.json", "w") as f:
                    new_data = {"exists":True,"result":{"name":newspaper_name,"number":count}}
                    results[i] = new_data
                    json.dump(results,f,ensure_ascii=False,indent=4)
                    print(new_data)

                with open("newspapers.json", "w") as f:
                    json.dump(newspapers,f,ensure_ascii=False,indent=4)

            else:
                with open("results.json", "w") as f:
                    new_data = {"exists":False,"result":{}}
                    results[i] = new_data
                    json.dump(results,f,ensure_ascii=False,indent=4)

                print(new_data)

    #This will update the missing json data
    #If the json data is up to date,it will say that it is Fully Updated
    def find_missing(self):
        try:
            with open("results.json",'r') as f:
                numbers = json.load(f)
        except FileNotFoundError:
            self.find_all(n1=self.minimum,n2=self.maximum)
        else:
            numbers = [int(number) for number in numbers]
            greatest = max(numbers)
            if greatest == self.maximum:
                print("Fully Updated")
            elif greatest < self.maximum:
                self.find_all(n1=greatest+1,n2=self.maximum)


    #This method will download the nth numbered url on the archive
    def download(self,data:dict,number:int):
        if data["exists"] == True:
            name = data["result"]["name"]
            count = data["result"]["number"]
            filename = f"{number} {name} ({count})"

            response = requests.get(url=f'http://press.natlib.uz/download.php?id={number}')
            try:
                os.makedirs(name)
            except FileExistsError:
                pass

            if response.status_code == 200:
                with open(f"{name}/{filename}.pdf","wb") as f:
                    f.write(response.content)
                with open("download_results.txt","a") as f:
                    f.write(f"{number} with name {filename} was downloaded\n")
                print(f"{number} with {filename}.pdf was downloaded")
        else:
            with open("download_results.txt","a") as f:
                f.write(f"{number} cannot be downloaded\n")
            print(f"{number} cannot be downloaded")

    #This method will download all the numbers from n1 till n2
    #download_n1_n2(1000,1005) will end up downloading the following numbers:
    #1000 1001 1002 1003 1004 1005
    def download_n1_n2(self,n1:int,n2:int):
        with open("results.json", "r") as f:
            newspapers = json.load(f)
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for i in range(n1,n2+1):
            self.download(newspapers[str(i)],i)

    #This method downloads the entire archive
    def download_all(self):
        self.download_n1_n2(n1=self.minimum,n2=self.maximum)


    #This method will download the entire newspaper
    def download_newspaper(self,newspaper:str):
        if newspaper in self.newspapers:
            with open("results.json", "r") as f:
                all_newspapers:dict = json.load(f)


            for (key,value) in all_newspapers.items():
                if value["exists"] == True:
                    if value["result"]["name"] == newspaper:
                        print(value,int(key))
                        self.download(data=value,number=int(key))

if __name__ == "__main__":
    unl = UzbekistanNationalLibrary()
    unl.find_missing()