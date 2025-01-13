# Gazete Kadıköy pdf webscraper
# Gazete Kadıköy is a local newspaper of Kadıköy, a municipality of Istanbul on the Asian side


import requests, os, lxml
from bs4 import BeautifulSoup


class GazeteKadikoy:
    def __init__(self):
        self.first = 1
        self.last = self.find_last()
        print(f"{self.last} is the last number")
        self.links = self.get_all_links()[::-1]

    # This will find the number of the last page of the archive
    def find_last(self) -> int:
        # when I last checked the archive had 59 pages
        count = 59
        found = False
        while not found:
            page = f"https://www.gazetekadikoy.com.tr/e-gazete?page={count}&filter=&filter="
            soup = BeautifulSoup(requests.get(url=page).text, "lxml")
            pages = [int(link.text) for link in soup.find_all("a", href=True, class_="page-link") if '«' not in link.text and '»' not in link.text]
            print(pages)
            largest = max(pages)
            if count > largest:
                found = True
            else:
                count = largest
        return count

    # This method will receive some text and output an integer with the numbers that were in the text
    # For example, this method with a text with "1308. number"
    # will return 1308 as an integer
    def get_number(self, text: str) -> int:
        output = ""
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        numbers = [str(n) for n in numbers]

        for char in text:
            if char in numbers:
                output += char
            else:
                pass

        return int(output)

    # This method will find the nth numbered page's newspaper links
    def find_pagelinks(self, page_number: int) -> list:
        page = f"https://www.gazetekadikoy.com.tr/e-gazete?page={page_number}&filter=&filter="
        soup = BeautifulSoup(requests.get(url=page).text, "lxml")
        links = []
        for link in soup.find_all("a", href=True, title=True, target=True):
            download_link = f'https://www.gazetekadikoy.com.tr{link["href"]}'.replace("\\", "/")
            number = link["title"]
            number = self.get_number(number)
            
            #if the number is zero, that means the pdf cannot be downloaded
            if number == 0:
                pass
            #The number should be 899
            elif number == 890 and download_link == "https://www.gazetekadikoy.com.tr/Uploads/gazetekadikoy.com.tr/e-gazete/dosya/22345678902142.pdf":
                t = 899, download_link
                links.append(t)
            #The number should be 995
            elif number == 955 and download_link == "https://www.gazetekadikoy.com.tr/Uploads/gazetekadikoy.com.tr/e-gazete/dosya/22345678902249.pdf":
                t = 995,download_link
                links.append(t)
            else:
                t = number, download_link
                links.append(t)
        return links

    # This will find all the newspaper links
    def get_all_links(self) -> list:
        links = []
        for i in range(self.first, self.last + 1):
            new = self.find_pagelinks(i)
            print(new)
            links += new
        return links

    # When given a tuple where,
    # The zeroth index is the number of the newspaper
    # The first index is the number of the download link
    # It will make a file named the number of the newspaper
    # Inside the file it will have pdf of the newspaper
    def download_tuple(self, count_link: tuple):
        count = str(count_link[0])
        link = count_link[1]
        print(count)
        os.makedirs(count)
        response = requests.get(url=link)

        if response.status_code == 200:
            with open(f"{count}/{count}.pdf", "wb") as f:
                f.write(response.content)
            with open("download_results.txt", "a") as f:
                f.write(f"{count}.pdf was downloaded\n")
            print(f"{count}.pdf was downloaded")
        else:
            with open("download_results.txt", "a") as f:
                f.write(f"{count}.pdf was not downloaded,it had response status code {response.status_code}\n")
            print(f"{count}.pdf was not downloaded,it had response status code {response.status_code}")


    # This method will download all of n1 till n2
    # download_n1_n2(500,505) will download all of:
    # 500 501 502 503 504 505 of Gazete Kadıköy
    def download_n1_n2(self, n1: int, n2: int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c

        for link in self.links:
            number = link[0]
            if n1 <= number <= n2:
                self.download_tuple(link)

    # This will downlaod the entire archive of Gazete Kadıköy
    def download_all(self):
        self.download_n1_n2(self.links[-1][0], self.links[0][0])

    # This method will download the nth number of Gazete Kadıköy
    # download_number(500) will download the number 500 of Gazete Kadıköy
    def download_number(self, number: int):
        for link in self.links:
            if link[0] == number:
                self.download_tuple(link)

    # This method will download the latest copy of Gazete Kadıköy
    def download_latest(self):
        self.download_tuple(self.links[-1])

    # The following method will check a specific number
    def check_number(self,number:int):
        for link in self.links:
            if link[0] == number:
                self.check_tuple(link)

    # The following method will check if the file had been downloaded before or not
    def check_tuple(self,link:tuple):
        count = str(count_link[0])
        link = count_link[1]
        print(count)
        try:
            os.mkdir(count)
        except FileExistsError:
            pass

        if f"{count}.pdf" not in os.listdir(count):
            response = requests.get(url=link)

            if response.status_code == 200:
                with open(f"{count}/{count}.pdf", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{count}.pdf was downloaded\n")
                print(f"{count}.pdf was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{count}.pdf was not downloaded,it had response status code {response.status_code}\n")
                print(f"{count}.pdf was not downloaded,it had response status code {response.status_code}")

    # The following method will check from one number to another larger number
    def check_n1_n2(self,n1:int,n2:int):
        if n1 > n2:
            c = n1
            n1 = n2
            n2 = c
        for i in range(n1,n2):
            self.check_number(i)

    # The following method will check the entire archive
    def check_all(self):
        numbers = [n[0] for n in self.links]
        n1 = min(numbers)
        n2 = max(numbers)
        self.check_n1_n2(n1,n2)

if __name__ == "__main__":
    gk = GazeteKadikoy()
    #gk.download_n1_n2(995, gk.links[-1][0])
    
