# Магнитогорский металл archive

import datetime,requests,lxml,os


class MagnitogorskyMetal:
    def __init__(self):
        self.start_date = datetime.datetime(day=2,month=10,year=1935)
        self.today = self.return_today()
        self.one_day = datetime.timedelta(days=1)

    # The following method will return today's date
    def return_today(self):
        t = datetime.datetime.now()
        day = t.day
        month = t.month
        year = t.year
        return  datetime.datetime(day=day,month=month,year=year)

    # The following method will check if there is a pdf for that particular date
    def download_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            if day < 10:
                day = f"0{day}"

            if month < 10:
                month = f"0{month}"

            filename = f'{year}-{month}-{day}.pdf'
            pdf_link = f"https://magmetall.ru/upload/archive_cache/{filename}"
            pdf_response = requests.get(url=pdf_link)
            if pdf_response.status_code == 200:
                with open(f"{filename}",'wb') as f:
                    f.write(pdf_response.content)
                with open('download_results.txt','a') as f:
                    f.write(f'{filename} was downloaded.\n')
                print(f'{filename} was downloaded.')
            elif pdf_response.status_code == 404:
                with open('download_results.txt','a') as f:
                    f.write(f'{filename} does not exist.\n')
                print(f'{filename} does not exist.')
            else:
                with open('download_results.txt', 'a') as f:
                    f.write(f'{filename} was not downloaded, it had response status code {pdf_response.status_code}\n')
                print(f'{filename} was not downloaded, it had response status code {pdf_response.status_code}')

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

    # The following method will check a particular date to see if it has been downloaded or not
    def check_date(self,date:datetime.datetime):
        if self.start_date <= date <= self.today:
            day = date.day
            month = date.month
            year = date.year

            if day < 10:
                day = f"0{day}"

            if month < 10:
                month = f"0{month}"

            filename = f'{year}-{month}-{day}.pdf'
            if filename not in os.listdir():
                pdf_link = f"https://magmetall.ru/upload/archive_cache/{filename}"
                pdf_response = requests.get(url=pdf_link)
                if pdf_response.status_code == 200:
                    with open(f"{filename}",'wb') as f:
                        f.write(pdf_response.content)
                    with open('download_results.txt','a') as f:
                        f.write(f'{filename} was downloaded.\n')
                    print(f'{filename} was downloaded.')
                elif pdf_response.status_code == 404:
                    with open('download_results.txt','a') as f:
                        f.write(f'{filename} does not exist.\n')
                    print(f'{filename} does not exist.')
                else:
                    with open('download_results.txt', 'a') as f:
                        f.write(f'{filename} was not downloaded, it had response status code {pdf_response.status_code}\n')
                    print(f'{filename} was not downloaded, it had response status code {pdf_response.status_code}')

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
        self.check_d1_d2(self.start_date, self.today)

if __name__ == "__main__":
    mm = MagnitogorskyMetal()
    mm.check_d1_d2(self=)

