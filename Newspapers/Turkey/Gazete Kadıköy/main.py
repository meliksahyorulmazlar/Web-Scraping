#Gazete Kadıköy pdf webscraper
#Gazete Kadıköy is a local newspaper of Kadıköy, a municipality of Istanbul on the Asian side


import requests,os,lxml
from bs4 import BeautifulSoup




class GazeteKadikoy:
    def __init__(self):
        self.first = 1
        self.last = self.find_last()

    #This will find the number of the last page of the archive
    def find_last(self)->int:
        #when I last checked the archive had 59 pages
        count = 59
        found = False
        while not found:
            page = f"https://www.gazetekadikoy.com.tr/e-gazete?page={count}&filter=&filter="
            soup = BeautifulSoup(requests.get(url=page).text,"lxml")
            pages = [int(link.text) for link in soup.find_all("a",href=True,class_="page-link") if '«' not in link.text and '»' not in link.text]
            print(pages)
            largest = max(pages)
            if count > largest:
                found = True
            else:
                count = largest
        return count

    def get_number(self,text:str)->int:
        output = ""
        numbers = [0,1,2,3,4,5,6,7,8,9]
        numbers = [str(n) for n in numbers]

        for char in text:
            if char in numbers:
                output += char
            else:
                pass

        return int(output)

    def find_pagelinks(self,page_number:int)->list:
        page = f"https://www.gazetekadikoy.com.tr/e-gazete?page={page_number}&filter=&filter="
        soup = BeautifulSoup(requests.get(url=page).text,"lxml")
        links = []
        for link in soup.find_all("a",href=True,title=True,target=True):
            download_link = f'https://www.gazetekadikoy.com.tr{link["href"]}'.replace("\\", "/")

            number = link["title"]

            number = self.get_number(number)

            t = number,download_link

            links.append(t)
        return links

    def get_all_links(self)->list:
        links = []
        for i in range(self.first,self.last+1):
            new =  self.find_pagelinks(i)
            print(new)
            links += new
        return links


    def download_tuple(self,count_link:tuple):
        count = str(count_link[0])
        link = count_link[1]

        os.makedirs(count)

        response = requests.get(url=link)

        if response.status_code == 200:
            with open(f"{count}/{count}.pdf","wb") as f:
                f.write(response.content)
            with open("download_results.txt","a") as f:
                f.write(f"{count}.pdf was downloaded\n")
            print(f"{count}.pdf was downloaded")
        else:
            with open("download_results.txt","a") as f:
                f.write(f"{count}.pdf was not downloaded,it had response status code {response.status_code}\n")
            print(f"{count}.pdf was not downloaded,it had response status code {response.status_code}")

    def download_all(self):
        links = self.get_all_links()[::-1]
        for link in links:
            print(link)
            self.download_tuple(link)



if __name__ == "__main__":
    gk = GazeteKadikoy()
    gk.download_all()
