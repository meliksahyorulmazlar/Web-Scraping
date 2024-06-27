import requests,lxml,os
from bs4 import BeautifulSoup


#webscraping all of Javan a newspaper in Iran
def get_data(number:int)->tuple:
    website = f"https://www.javanonline.ir/fa/publications?type_id=1&publication_id=1&issue_id={number}"
    soup = BeautifulSoup(requests.get(website).text, "lxml")
    attribute = "/files/fa/publication/pages/"
    pdf_links = list(set([f'https://www.javanonline.ir{link["href"]}' for link in soup.find_all("a", href=True) if attribute and "pdf" in link["href"]]))
    file_name = soup.find("div", class_="col-md-23 col-xs-36").text.strip()
    os.makedirs(file_name)
    return file_name,pdf_links



def download_links(pdf_links:list,file_name:str)->None:
    for pdf_link in pdf_links:
        pdf_name = pdf_link.split("/")[-1]
        response = requests.get(url=pdf_link)
        if response.status_code == 200:
            with open(f"{file_name}/{pdf_name}", "wb") as f:
                f.write(response.content)
            with open("javan.txt", "a") as f:
                f.write(f"{file_name} {pdf_name} was downloaded\n")
            print(f"{file_name} {pdf_name} was downloaded")
        else:
            with open("javan.txt", "a") as f:
                f.write(f"{file_name} {pdf_name} had a response status code of {response.status_code}\n")
            print(f"{file_name} {pdf_name} had a response status code of {response.status_code}")


if __name__ == "__main__":
    main_page = "https://www.javanonline.ir"
    s = BeautifulSoup(requests.get(url=main_page).text,"lxml")
    image_tag = [tag["src"] for tag in s.find_all("img",src=True) if "/files/fa/publication/issues/" in tag["src"]][0]
    current_number = int(image_tag.rstrip(".png").split("_")[-1]) +1

    for i in range(37,current_number):
        try:
            data = get_data(i)
        except AttributeError:
            print("No pdfs for that link")
            with open("javan.txt","a") as f:
                f.write(f"No pdfs for that link https://www.javanonline.ir/fa/publications?type_id=1&publication_id=1&issue_id={i}\n")
            continue
        else:
            name = data[0]
            links = data[1]
            download_links(pdf_links=links,file_name=name)



