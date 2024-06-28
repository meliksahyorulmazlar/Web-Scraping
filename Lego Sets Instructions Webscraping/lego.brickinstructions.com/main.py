import requests,lxml,os
from bs4 import BeautifulSoup
#code to webscrape lego instructions from https://lego.brickinstructions.com

class BrickInstructions:

    #this method gets a text file of all the sets for each year from 1965 to 2023
    #plus it gets a file called all_sets.txt with all the lego sets on the website on a single text file
    def get_texts(self)->None:

        possible_pages = [str(i) for i in range(1, 19)]
        years_page = "https://lego.brickinstructions.com/en/showallyears"
        soup = BeautifulSoup(requests.get(url=years_page).text,'lxml')
        year_links = sorted([tag["href"] for tag in soup.find_all("a",href=True) if "year" in tag["href"]])[2:]

        for year_link in year_links:

            year = year_link.split("/")[-1]

            year_soup = BeautifulSoup(requests.get(url=year_link).text,"lxml")
            pages = [anchor_tag["href"] for anchor_tag in year_soup.find_all("a",href=True) if anchor_tag.text in possible_pages]

            if len(pages) == 0:
                products = list(set([product["href"] for product in year_soup.find_all("a",href=True,class_="thumbLink")]))
                for product in products:
                    with open(f"{year}.txt","a") as f:
                        f.write(f"{product}\n")
                    with open("all_sets.txt","a") as f:
                        f.write(f"{product}\n")
                    print(product)
            else:
                for page in pages:
                    page_soup = BeautifulSoup(requests.get(url=page).text,"lxml")
                    products = list(set([product["href"] for product in page_soup.find_all("a",href=True,class_="thumbLink")]))
                    for product in products:
                        with open(f"{year}.txt", "a") as f:
                            f.write(f"{product}\n")
                        with open("all_sets.txt", "a") as f:
                            f.write(f"{product}\n")
                            print(product)

    #this will download all the lego sets found on the website for that year from 1965 to 2023
    def download_year(year:str)->None:
        year_link = f"https://lego.brickinstructions.com/search/year/{year}"

        year_soup = BeautifulSoup(requests.get(url=year_link).text, "lxml")
        pages = [anchor_tag["href"] for anchor_tag in year_soup.find_all("a", href=True) if anchor_tag.text in possible_pages]

        lego_sets = []
        if len(pages) == 0:
            products = [product["href"] for product in year_soup.find_all("a", href=True, class_="thumbLink")]
            products = list(set(products))
            for product in products:
                lego_sets.append(product)
        else:
            for page in pages:
                page_soup = BeautifulSoup(requests.get(url=page).text, "lxml")
                products = [product["href"] for product in page_soup.find_all("a", href=True, class_="thumbLink")]
                products = list(set(products))
                for product in products:
                    lego_sets.append(product)

        if len(lego_sets) > 0:
            os.makedirs(year)
            for lego_set in lego_sets:

                set_soup = BeautifulSoup(requests.get(url=lego_set).text,"lxml")
                photos = [anchor["href"] for anchor in set_soup.find_all("a",href=True,class_="fancybox")]

                set_name = lego_set.split("/")[-1]
                set_number = lego_set.split("/")[-2]

                file_name = f"{set_number} {set_name}"
                os.makedirs(f"{year}/{file_name}")
                for photo in photos:

                    response = requests.get(photo)
                    photo_file = photo.split("/")[-1]
                    if response.status_code == 200:
                        with open(f"{year}/{file_name}/{photo_file}","wb") as f:
                            f.write(response.content)
                        with open("results.txt","a") as f:
                            f.write(f"{year}/{file_name}/{photo_file} was downloaded\n")
                        print(f"{year}/{file_name}/{photo_file} was downloaded\n")

                    else:
                        with open("results.txt","a") as f:
                            f.write(f"{year}/{file_name}/{photo_file} had response {response.status_code}\n")
                        print(f"{year}/{file_name}/{photo_file} had response {response.status_code}\n")

    #This method downloads all of the instructions from 1965-2023 found on the website
    #will be in files from 1965 to 2023
    def download_all(self)->None:
        for i in range(1965,2024):
            year = str(i)
            year_link = f"https://lego.brickinstructions.com/search/year/{year}"

            year_soup = BeautifulSoup(requests.get(url=year_link).text, "lxml")
            pages = [anchor_tag["href"] for anchor_tag in year_soup.find_all("a", href=True) if anchor_tag.text in possible_pages]

            lego_sets = []
            if len(pages) == 0:
                products = [product["href"] for product in year_soup.find_all("a", href=True, class_="thumbLink")]
                products = list(set(products))
                for product in products:
                    lego_sets.append(product)
            else:
                for page in pages:
                    page_soup = BeautifulSoup(requests.get(url=page).text, "lxml")
                    products = [product["href"] for product in page_soup.find_all("a", href=True, class_="thumbLink")]
                    products = list(set(products))
                    for product in products:
                        lego_sets.append(product)

            if len(lego_sets) > 0:
                os.makedirs(year)
                for lego_set in lego_sets:

                    set_soup = BeautifulSoup(requests.get(url=lego_set).text, "lxml")
                    photos = [anchor["href"] for anchor in set_soup.find_all("a", href=True, class_="fancybox")]

                    set_name = lego_set.split("/")[-1]
                    set_number = lego_set.split("/")[-2]

                    file_name = f"{set_number} {set_name}"
                    os.makedirs(f"{year}/{file_name}")
                    for photo in photos:

                        response = requests.get(photo)
                        photo_file = photo.split("/")[-1]
                        if response.status_code == 200:
                            with open(f"{year}/{file_name}/{photo_file}", "wb") as f:
                                f.write(response.content)
                            with open("results.txt", "a") as f:
                                f.write(f"{year}/{file_name}/{photo_file} was downloaded\n")
                            print(f"{year}/{file_name}/{photo_file} was downloaded\n")

                        else:
                            with open("results.txt", "a") as f:
                                f.write(f"{year}/{file_name}/{photo_file} had response {response.status_code}\n")
                            print(f"{year}/{file_name}/{photo_file} had response {response.status_code}\n")

    #this method will print out the lego category links and names
    def get_lego_categories(self)->None:
        category_page = "https://lego.brickinstructions.com/en/categoryList"

        category_soup = BeautifulSoup(requests.get(url=category_page).text,"lxml")

        category_links = [link["href"] for link in category_soup.select(selector="td a",href=True)]

        category_names = [link.text for link in category_soup.select(selector="td a",href=True)]

        print(category_links)
        print(category_names)

    #Downloads an entire lego category when given the correct link
    def download_category(self,link:str):
        category_page = "https://lego.brickinstructions.com/en/categoryList"

        category_soup = BeautifulSoup(requests.get(url=category_page).text, "lxml")

        category_links = [link["href"] for link in category_soup.select(selector="td a", href=True)]

        if link in category_links:

            category_names = [link.text for link in category_soup.select(selector="td a", href=True)]

            index = category_links.index(link)
            category = category_names[index]


            category_link = f"https://lego.brickinstructions.com/en/lego_instructions/theme/{link}"


            category_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
            possible_pages = [str(i) for i in range(1, 38)]
            pages = [anchor_tag["href"] for anchor_tag in category_soup.find_all("a", href=True) if anchor_tag.text in possible_pages]
            lego_sets = []
            if len(pages) == 0:
                products = [product["href"] for product in  category_soup.find_all("a", href=True, class_="thumbLink")]
                products = list(set(products))
                for product in products:
                    lego_sets.append(product)
            else:
                for page in pages:
                    page_soup = BeautifulSoup(requests.get(url=page).text, "lxml")
                    products = [product["href"] for product in page_soup.find_all("a", href=True, class_="thumbLink")]
                    products = list(set(products))
                    for product in products:
                        lego_sets.append(product)

            if len(lego_sets) > 0:
                os.makedirs(category)
                for lego_set in lego_sets:

                    set_soup = BeautifulSoup(requests.get(url=lego_set).text, "lxml")
                    photos = [anchor["href"] for anchor in set_soup.find_all("a", href=True, class_="fancybox")]

                    set_name = lego_set.split("/")[-1]
                    set_number = lego_set.split("/")[-2]

                    file_name = f"{set_number} {set_name}"
                    os.makedirs(f"{category}/{file_name}")
                    for photo in photos:

                        response = requests.get(photo)
                        photo_file = photo.split("/")[-1]
                        if response.status_code == 200:
                            with open(f"{category}/{file_name}/{photo_file}", "wb") as f:
                                f.write(response.content)
                            with open("results.txt", "a") as f:
                                f.write(f"{category}/{file_name}/{photo_file} was downloaded\n")
                            print(f"{category}/{file_name}/{photo_file} was downloaded\n")

                        else:
                            with open("results.txt", "a") as f:
                                f.write(f"{category}/{file_name}/{photo_file} had response {response.status_code}\n")
                            print(f"{category}/{file_name}/{photo_file} had response {response.status_code}\n")

    # This method downloads all of the instructions for every category
    # will be in files for every lego category
    #when done you should end up with 188 Files with all the categories
    def download_categories(self)->None:
        category_page = "https://lego.brickinstructions.com/en/categoryList"

        category_soup = BeautifulSoup(requests.get(url=category_page).text, "lxml")

        category_links = [link["href"] for link in category_soup.select(selector="td a", href=True)]

        category_names = [link.text for link in category_soup.select(selector="td a", href=True)]

        for link in category_links:
            category_names = [link.text for link in category_soup.select(selector="td a", href=True)]

            index = category_links.index(link)
            category = category_names[index]

            category_link = f"https://lego.brickinstructions.com/en/lego_instructions/theme/{link}"

            category_soup = BeautifulSoup(requests.get(url=link).text, "lxml")
            possible_pages = [str(i) for i in range(1, 38)]
            pages = [anchor_tag["href"] for anchor_tag in category_soup.find_all("a", href=True) if
                     anchor_tag.text in possible_pages]
            lego_sets = []
            if len(pages) == 0:
                products = [product["href"] for product in category_soup.find_all("a", href=True, class_="thumbLink")]
                products = list(set(products))
                for product in products:
                    lego_sets.append(product)
            else:
                for page in pages:
                    page_soup = BeautifulSoup(requests.get(url=page).text, "lxml")
                    products = [product["href"] for product in page_soup.find_all("a", href=True, class_="thumbLink")]
                    products = list(set(products))
                    for product in products:
                        lego_sets.append(product)
            

            if len(lego_sets) > 0:
                os.makedirs(category)
                for lego_set in lego_sets:

                    set_soup = BeautifulSoup(requests.get(url=lego_set).text, "lxml")
                    photos = [anchor["href"] for anchor in set_soup.find_all("a", href=True, class_="fancybox")]

                    set_name = lego_set.split("/")[-1]
                    set_number = lego_set.split("/")[-2]

                    file_name = f"{set_number} {set_name}"
                    os.makedirs(f"{category}/{file_name}")
                    for photo in photos:

                        response = requests.get(photo)
                        photo_file = photo.split("/")[-1]
                        if response.status_code == 200:
                            with open(f"{category}/{file_name}/{photo_file}", "wb") as f:
                                f.write(response.content)
                            with open("results.txt", "a") as f:
                                f.write(f"{category}/{file_name}/{photo_file} was downloaded\n")
                            print(f"{category}/{file_name}/{photo_file} was downloaded\n")

                        else:
                            with open("results.txt", "a") as f:
                                f.write(f"{category}/{file_name}/{photo_file} had response {response.status_code}\n")
                            print(f"{category}/{file_name}/{photo_file} had response {response.status_code}\n")


if __name__ == "__main__":
    bi = BrickInstructions()

    #The following method will download all the instructions and all the instructions will be inside of categories such as lego city,jurassic park et cetera
    #takes no inputs
    # This method will download all the lego set instructions
    # However, the lego sets will be put into files on to the respective category that they are part of
    #bi.download_categories()

    #The following method will print all the category links and names
    #takes no inputs
    #bi.get_lego_categories()

    #The following method will download a specific category that will be mentioned in the input
    #Takes a link input. Have a look at the following
    #https://lego.brickinstructions.com/en/lego_instructions/theme/lego_city will download lego city
    #You can go to https://lego.brickinstructions.com for more categories or use the get_lego_categories() method to find the other lego categories
    #bi.download_category(link="https://lego.brickinstructions.com/en/lego_instructions/theme/lego_city")

    #This method will get 2 sorts of files:
    #One will be all_sets.txt which will have all the lego sets from 1965 to 2023 on a single file
    #The other sort of file will be a yearly file which will be a text file for every year on a separate text file
    #So for example all the lego sets for 1970 will be on a text file called 1970.txt (there will be text files from 1965.txt to 2023.txt)
    #takes no input
    #bi.get_texts()

    #This method will download the lego sets found on that year
    #The input will take a string (the year should be anything from 1965 to 2023)
    #bi.download_year("1983")

    #This method will download all the lego set instructions
    #However, the lego sets will be put into files on to the respective year that they were released in
    #takes no input
    #bi.download_all()



