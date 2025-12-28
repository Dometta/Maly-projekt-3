import pandas as pd
import requests
import zipfile
import io


class DownloadCleanData:
    def __init__(self, years):
        self.meta_url = "https://powietrze.gios.gov.pl/pjp/archives/downloadFile/584"
        self.gios_archive_url = "https://powietrze.gios.gov.pl/pjp/archives/downloadFile/"
        self.gios_id = {2014: '302', 2019: '322', 2024: '582'}
        self.gios_pm25_file = {
            2014: '2014_PM2.5_1g.xlsx',
            2019: '2019_PM25_1g.xlsx',
            2024: '2024_PM25_1g.xlsx'
        }
        self.years = years
        self.data = {}              # oczyszczone dane roczne
        self.common_stations = None
        self.df_all_years = None

    # --------------------------------------------------
    # Pobieranie archiwum GIOŚ
    # --------------------------------------------------
    def download_gios_archive(self, year):
        url = f"{self.gios_archive_url}{self.gios_id[year]}"
        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open(self.gios_pm25_file[year]) as f:
                df = pd.read_excel(f, header=None)

        return df

    # --------------------------------------------------
    # Czyszczenie danych
    # --------------------------------------------------
    def clean_data(self, df):
        df = df.set_index(0)

        if {'Kod stanowiska', 'Jednostka', 'Nr'}.issubset(df.index):
            df = df.drop(['Wskaźnik', 'Kod stanowiska',
                           'Czas uśredniania', 'Jednostka', 'Nr'])
        else:
            df = df.drop(['Wskaźnik', 'Czas uśredniania'])

        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df.index = pd.to_datetime(df.index)

        df.index = [
            idx - pd.Timedelta(days=1) if idx.hour == 0 else idx
            for idx in df.index
        ]

        df.index.name = "Data poboru danych"
        return df

    # --------------------------------------------------
    # Metadane + słownik mapowania
    # --------------------------------------------------
    def download_metadata(self):
    
        # Pobranie pliku
        #response = requests.get(self.meta_url)
        #response.raise_for_status()
    
        # Zapisanie tymczasowo na dysku
        #temp_file = "metadane.xlsx"
        #with open(temp_file, "wb") as f:
            #f.write(response.content)
    
        # Wczytanie pliku Excel
        metadane = pd.read_excel("metadane.xlsx")  # Pandas sam dobierze silnik
    
        # Czyszczenie i przygotowanie metadanych
        cols = list(metadane.columns)
        cols[4] = 'Stary kod'
        metadane.columns = cols
    
        metadane = metadane.dropna(subset=['Stary kod'])
        metadane['Stary kod'] = metadane['Stary kod'].str.split(', ')
        metadane = metadane.explode('Stary kod')
    
        return metadane


    def mapping(self, df, mapping_dict):
        df.columns = df.columns.map(lambda x: mapping_dict.get(x, x))
        return df

    # --------------------------------------------------
    # Pobranie + czyszczenie + mapowanie
    # --------------------------------------------------
    def download_all(self):
        metadane = self.download_metadata()

        mapping_dict = dict(
            zip(metadane['Stary kod'], metadane['Kod stacji'])
        )

        for year in self.years:
            df = self.download_gios_archive(year)
            df = self.clean_data(df)
            df = self.mapping(df, mapping_dict)
            self.data[year] = df

    

    # --------------------------------------------------
    # Wspólne stacje
    # --------------------------------------------------
    def get_common_stations(self):
        dfs = list(self.data.values())
        common = dfs[0].columns

        for df in dfs[1:]:
            common = common.intersection(df.columns)

        self.common_stations = common
        return common
    
    
    # --------------------------------------------------
    # MultiIndex (Kod stacji, Miejscowość)
    # --------------------------------------------------
    def make_multi_index(self, metadane):
        # Filtrujemy tylko te stacje, które są wspólne
        filtered = metadane[metadane['Kod stacji'].isin(self.common_stations)]
        
        # Usuwamy duplikaty Kodów Stacji, żeby mieć dokładnie 1 wiersz na stację
        filtered_unique = filtered.drop_duplicates(subset=['Kod stacji'])
        
        # Sortujemy metadane tak samo jak kolumny w danych
        # Tworzymy słownik pomocniczy, żeby zachować kolejność z self.common_stations
        mapping_dict = dict(zip(filtered_unique['Kod stacji'], filtered_unique['Miejscowość']))
        
        station_city = [
            (st_code, mapping_dict.get(st_code, "Nieznana")) 
            for st_code in self.common_stations
        ]
        
        multi_index = pd.MultiIndex.from_tuples(
            station_city,
            names=['Kod stacji', 'Miejscowość']
        )
        
        return multi_index

    # --------------------------------------------------
    # Finalne dane do analizy
    # --------------------------------------------------
    def prepare_common_data(self):
        metadane = self.download_metadata()
        self.get_common_stations()

        multi_index = self.make_multi_index(metadane)

        dfs_common = []
        for year in self.years:
            df = self.data[year][self.common_stations]
            df.columns = multi_index
            dfs_common.append(df)

        self.df_all_years = pd.concat(dfs_common)
        return self.df_all_years

  
