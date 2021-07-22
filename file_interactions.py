from zipfile import ZipFile
from csv import DictReader
import requests
import os


class FileInteractions:
    def __init__(self, zip_path, folder_path, url):
        self.zip_path = zip_path
        self.folder_path = folder_path
        self.url = url


    def download_url(self, chunk_size=128):
        r = requests.get(self.url, stream=True)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        with open(self.zip_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)


    def extract_csv(self):
        file_name = ''
        with ZipFile(self.zip_path,'r') as myzip:
            file_name = myzip.namelist()[0]
            myzip.extractall(self.folder_path)
        os.remove(self.zip_path)
        return file_name


    def get_csv_date(self, file_name):
        from datetime import datetime
        date_vals = file_name[:6]
        return datetime.strptime(date_vals, '%y%m%d')

    def get_indicators(self, cities, file_name):
        with open(f'{self.folder_path}/{file_name}', 'r', encoding="ISO-8859-1") as csv_f:
            f = DictReader(csv_f)
            for row in f:
                city_index = (int(row['MUNICIPIO_RES']), int(row['ENTIDAD_RES']))
                if city_index in cities:
                    if int(row['RESULTADO']) == 1:
                        cities[city_index]['confirmed'] += 1
        return cities

    
    def confirmed(self, row, date):
        if int(row['RESULTADO']) == 1:
            pass            
