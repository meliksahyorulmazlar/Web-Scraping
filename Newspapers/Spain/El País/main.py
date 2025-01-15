# El País is a newspaper in Spain
import datetime,requests
import os


class ElPais:
    def __init__(self):
        self.start_date = datetime.datetime(day=4,month=5,year=1976)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    # The following method will return today's date
    def return_today(self)->datetime.datetime:
        time = datetime.datetime.now()
        day = time.day
        month = time.month
        year = time.year
        return datetime.datetime(day=day,month=month,year=year)

    # The following method will download a specific date's image or pdf if it exists
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = str(date.day)
            if len(day) == 1:
                day = f"0{day}"
            month = str(date.month)
            if len(month) == 1:
                month = f"0{month}"
            year = str(date.year)

            try:
                os.mkdir(year)
            except FileExistsError:
                pass

            image_link = f'https://srv00.epimg.net/pdf/elpais/snapshot/{year}/{month}/elpais/{year}{month}{day}Big.jpg'
            pdf_link = f'https://srv00.epimg.net/pdf/elpais/1aPagina/{year}/{month}/ep-{year}{month}{day}.pdf'
            main = f"{day}-{month}-{year}"
            image_file = f"{main}.jpg"
            pdf_file = f"{main}.pdf"
            image_response = requests.get(image_link)
            if image_response.status_code == 200:
                os.mkdir(f"{year}/{main}")
                with open(f"{year}/{main}/{image_file}",'wb') as f:
                    f.write(image_response.content)
                with open('download_results.txt','a') as f:
                    f.write(f"{image_file} was downloaded.\n")
                print(f"{image_file} was downloaded.")
                pdf_response = requests.get(pdf_link)
                if pdf_response.status_code == 200:
                    with open(f"{year}/{main}/{pdf_file}", 'wb') as f:
                        f.write(pdf_response.content)
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{pdf_file} was downloaded.\n")
                    print(f"{pdf_file} was downloaded.")
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f"{main} had no pdf.\n")
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(f"There was no paper for {main}.\n")
                print(f"There was no paper for {main}.")

    # The following method will download from one date to another later date
    def download_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.download_date(d1)
            d1 += self.one_day

    # The following method will download the entire archive
    def download_all(self):
        self.download_d1_d2(self.start_date,self.today)

    # The following method will check if there is an image for a particular date
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            if self.start_date <= date <= self.today:
                day = str(date.day)
                if len(day) == 1:
                    day = f"0{day}"
                month = str(date.month)
                if len(month) == 1:
                    month = f"0{month}"
                year = str(date.year)

                try:
                    os.mkdir(year)
                except FileExistsError:
                    pass

                image_link = f'https://srv00.epimg.net/pdf/elpais/snapshot/{year}/{month}/elpais/{year}{month}{day}Big.jpg'
                pdf_link = f'https://srv00.epimg.net/pdf/elpais/1aPagina/{year}/{month}/ep-{year}{month}{day}.pdf'
                main = f"{day}-{month}-{year}"
                image_file = f"{main}.jpg"
                pdf_file = f"{main}.pdf"
                image_response = requests.get(image_link)
                if f"{main}" not in os.listdir(f"{year}"):
                    self.download_date(date)
                elif image_file not in os.listdir(f"{year}/{main}"):
                    image_response = requests.get(image_link)
                    if image_response.status_code == 200:
                        with open(f"{year}/{main}/{image_file}", 'wb') as f:
                            f.write(image_response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{image_file} was downloaded.\n")
                        print(f"{image_file} was downloaded.")
                        if pdf_file not in os.listdir(f"{year}/{main}"):
                            pdf_response = requests.get(pdf_link)
                            if pdf_response.status_code == 200:
                                with open(f"{year}/{main}/{pdf_file}", 'wb') as f:
                                    f.write(pdf_response.content)
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{pdf_file} was downloaded.\n")
                                print(f"{pdf_file} was downloaded.")
                            else:
                                with open('download_results.txt', 'a') as f:
                                    f.write(f"{main} had no pdf.\n")
                                print(f"{main} had no pdf.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"There was no paper for {main}.\n")
                        print(f"There was no paper for {main}.\n")
                elif pdf_file not in os.listdir(f"{year}/{main}"):
                    pdf_response = requests.get(pdf_link)
                    if pdf_response.status_code == 200:
                        with open(f"{year}/{main}/{pdf_file}", 'wb') as f:
                            f.write(pdf_response.content)
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{pdf_file} was downloaded.\n")
                        print(f"{pdf_file} was downloaded.")
                    else:
                        with open('download_results.txt', 'a') as f:
                            f.write(f"{main} had no pdf.\n")
                        print(f"{main} had no pdf.")

    # The following method will check from one date to another later date
    def check_d1_d2(self,d1:datetime.datetime,d2:datetime.datetime):
        if d1 > d2:
            c = d1
            d1 = d2
            d2 = c

        while d1 <= d2:
            self.check_date(d1)
            d1 += self.one_day

    # The following method will check the entire archive
    def check_all(self):
        self.check_d1_d2(self.start_date,self.today)

if __name__ == "__main__":
    ep = ElPais()
    ep.check_all()