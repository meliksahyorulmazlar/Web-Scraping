#webscraping all of Javan
#Javan is a newspaper in Iran
import requests,lxml,os
from bs4 import BeautifulSoup


class Javan:
    def __init__(self):
        self.latest = self.current()

    #This method finds the latest copy of Javan
    def current(self)->int:
        main_page = "https://www.javanonline.ir"
        s = BeautifulSoup(requests.get(url=main_page).text, "lxml")
        image_tag = [tag["src"] for tag in s.find_all("img", src=True) if "/files/fa/publication/issues/" in tag["src"]][0]
        return int(image_tag.rstrip(".png").split("_")[-1])

    #This will return a newspaper's name and it's pdf links as a tuple
    def get_data(self,number: int) -> tuple:
        website = f"https://www.javanonline.ir/fa/publications?type_id=1&publication_id=1&issue_id={number}"
        soup = BeautifulSoup(requests.get(website).text, "lxml")
        attribute = "/files/fa/publication/pages/"
        pdf_links = list(set([f'https://www.javanonline.ir{link["href"]}' for link in soup.find_all("a", href=True) if attribute and "pdf" in link["href"]]))
        file_name = soup.find("div", class_="col-md-23 col-xs-36").text.strip()
        os.makedirs(file_name)
        return file_name, pdf_links

    #This will download the pdfs of the newspaper
    def download_links(self,pdf_links: list, file_name: str) -> None:
        for pdf_link in pdf_links:
            pdf_name = pdf_link.split("/")[-1]
            response = requests.get(url=pdf_link)
            if response.status_code == 200:
                with open(f"{file_name}/{pdf_name}", "wb") as f:
                    f.write(response.content)
                with open("download_results.txt", "a") as f:
                    f.write(f"{file_name} {pdf_name} was downloaded\n")
                print(f"{file_name} {pdf_name} was downloaded")
            else:
                with open("download_results.txt", "a") as f:
                    f.write(f"{file_name} {pdf_name} had a response status code of {response.status_code}\n")
                print(f"{file_name} {pdf_name} had a response status code of {response.status_code}")

    #This method will check if there any pdfs for that newspaper number
    def download(self,i:int):
        try:
            data = self.get_data(i)
        except AttributeError:
            print("No pdfs for that link")
            with open("download_results.txt", "a") as f:
                f.write(f"No pdfs for that link https://www.javanonline.ir/fa/publications?type_id=1&publication_id=1&issue_id={i}\n")
        else:
            name = data[0]
            links = data[1]
            self.download_links(pdf_links=links, file_name=name)

    #This method will download all of Javan's archive
    def download_all(self):
        for i in range(37, self.latest + 1):
            self.download(i)

    #This will download the latest copy of Javan
    def download_latest(self):
        self.download(self.latest)

if __name__ == "__main__":
    javan = Javan()
    javan.download_latest()