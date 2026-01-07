# Maly-projekt-3

## Dokumentacja

### Całokształt

W tym repozytorium znajduje się plik ipynb - projekt_3.ipynb, który jest zmodyfikowaną wersją małego projektu nr 1.
Najważniejszą zmianą było przeniesienie części: pobierania danych, analizy danych, wizualizacji danych do odrębnych plików .py (w tej samej kolejności: DownloadClean.py, Analysis.py, Visualization.py) z których funkcje są importowane i po kolei odpalane w notatniku.
Obecne są równierz testy dla każdego z plików .py, znajdujące się w folderze tests. 
Są to: DownloadClean_test.py, Analysis_test.py, Visualization_test.py . 
Znajduje się również plik .gitignore, README.md zawierający dokumentację, plik z metadanymi - metadane_new.xlsx oraz oryginalny notatnik dla małego projektu nr 1 - projekt_1_student.ipynb

### Pliki .py

DownloadClean.py zawiera:
- stałe: URL dla metadanych i archiwów, ID i nazwy plików dla poszczególnych lat.
- funkcję download_gios_archive(year) -> df ; pobiera archiwum GIOŚ dla danego roku.
- funckję clean_data(df,year) -> df ; oczyszcza df z danymi w zależności od roku, shiftuje czas dla godziny 00:00:00 do 23:59:59 .
- funkcję download_metadata() -> df ; pobiera metadane ze strony GIOŚ.
- funkcję map_station_codes(df, mapping_dict) -> df ; mapuje kody stacji dla danego df.
- funkcję download_all(years) -> dict[year, df] ; przy pomocy powyższych funkcji pobiera, czyści i mapuje dane dla wszystkich lat znajdujących się w liście years, tworzy także mapping_dict używany przez funkcję map_stattion_codes.
- funkcję make_multi_index(metadane, common_stations) -> pd.MultiIndex ; Tworzy multiindex - indeks składający się z kodu stacji i miejscowości, jeżeli miasto jest nieznane - indeks tworzy kod stacji i "nieznane"
- funkcję prepare_common_data(years) -> df ; dla listy lat tworzy ostateczny df z multiindeksem - z połączonych df dla poszczególnych lat, który zapisuje do pliku .csv . Wykorzystuje do tego powyższe funkcje.

Analysis.py zawiera:
- stałą globalną: PM25_NORM=15 .
- funckję monthly_mean(df,years) -> df ; która grupując po latach i miesiącach oblicza średnie miesięczne dla lat-years, wyniki zwraca w tabeli gdzie rok i miesiąc są indeksami a wartością średnia.
- funkcję days_above_norm(df, norm) -> df ; kopiuje dane a następnie wyciąga datę bez godziny i umieszcza ją w nowej kolumnie. Grupując po nowej kolumnie oblicza średnią dzienną. Zwraca zmodyfikowaną o średnią kopię oryginalnego df.
- funkcję days_above_norm(df, norm) -> df ; dzięki średnim dobowym i grupowaniu po latach zlicza wystąpenia dni w których norma została przekroczona dla poszczególnych lat.

Visualization.py zawiera:
- funckję mean_pm25_plot(df, years) ; Wyodrębnia dane dla Katowic i Warszawy po czy oblicza dla nich średnie miesięczne dla wybranych lat. Generuje wykres liniowy porównujacy trendy miesięcznych stężeń PM2.5 dla Warszawy i Katowic w latach 2015 i 2024.
- funkcję heatmap(df, years) ; Tworzy heatmapy średnich miesięcznych dla wszytskich miast w zbiorze danych, dla danych lat.
- funkcję grouped_barplot(df) ; Tworzy zgrupowany wykres słupkowy dla 6 stacji o ekstremalnych wynikach (3 najlepszych i 3 najgorszych) dla roku 2024 .

### Testy 
Znajdują się w folderze tests

DownloadClean_test.py zawiera:
- funkcję test_clean_data_2015(), test_clean_data_2018(), test_clean_data_2021() ; Testują czy dla poszczególnych lat dobrze usuwane są niepotrzebne wartości.
- funkcję test_clean_data_midnight_shift() ; testuje czy dobrze zachodzi shiftowanie danych o północy.
- funkcję test_map_station_codes() ; test czy kody stacji odpowiednio się mapują.
- funkcję test_make_multi_index() ; test czy poprawnie tworzony jest multiindex.
- funkcję test_make_multi_index_unknown_city() ; test czy multiindex poprawnie się tworzy dla nieznanej miejscowości

Analysis_test.py zawiera:
- funkcję test_monthly_mean() ; testuje czy dobrze obliczane są średnie miesięczne.
- funkcję test_daily_mean() ; testuje czy dobrze obliczane są średnie dobowe.
- funkcję test_days_above_norm() ; testuje czy dobrze zliczane są dni w których norma została przekroczona.

Visualization_test.py zawiera: (utylizowany jest monkeypatch aby nie wyświetlać wykresów - wyłącznie sprawdzić czy funkcje w Visualization_py działają)

- funkcję test_mean_pm25_plot(monkeypatch) ; testuje czy poprawnie tworzy się wykres liniowy.
- funkcję test_heatmap(monkeypatch) ; testuje czy poprawnie tworzą się heatmapy.
- funkcję test_grouped_barplot_runs(monkeypatch) ; testuje czy poprawnie tworzy się barplot.

### Pozostałe pliki

- projekt_1_student.ipynb - oryginalny notatnik z małego projektu 1 z niepoprawionym kodem.
- projekt_3.ipynb - notatnik który dzięki funkcjom z plików .py, zawierającym poprawiony kod, wykonuje po kolei zadania małego projektu 1.
- metdane_new.xlsx - plik z metadanymi.



    
