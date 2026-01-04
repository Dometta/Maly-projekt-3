import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def mean_pm25_plot(df,years):
    # Wybieram odpowiednie miasta
    df_waw = df.xs('Warszawa', level='Miejscowość', axis=1)
    df_kat = df.xs('Katowice', level='Miejscowość', axis=1)
    
    df_waw_mean = df_waw.mean(axis=1)

    # Wybieram odpowiedni rok i miasto
    waw_2024 = df_waw_mean.xs(2024, level='Rok')
    kat_2024 = df_kat.xs(2024, level='Rok')
    waw_2014 =df_waw_mean.xs(2015, level='Rok')
    kat_2014 = df_kat.xs(2015, level='Rok')
    
    plt.figure(figsize=(10,6))
    
    plt.plot(waw_2014.index, waw_2014.values, label="Warszawa 2015", marker='o')
    plt.plot(waw_2024.index, waw_2024.values, label="Warszawa 2024", marker='o')
    plt.plot(kat_2014.index, kat_2014.values, label="Katowice 2015", marker='s')
    plt.plot(kat_2024.index, kat_2024.values, label="Katowice 2024", marker='s')
    
    plt.xlabel("Miesiąc", fontsize=14)
    plt.ylabel("Średnie PM2.5", fontsize=14)
    plt.title("Trend miesięcznych stężeń PM2.5 (Warszawa vs Katowice, 2015 i 2024)", fontsize=18)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xticks(range(1, 13))
    plt.tight_layout()
    plt.show()

def heatmap(df,years):
    df_city_month = df.groupby(level='Miejscowość', axis=1).mean() # grupowanie po mieście
    matrix_dict = {} # słownik na macierze dla poszczególnych miast

    for city in df_city_month.columns.values:
    
        matrix = df_city_month[city].unstack(level='Miesiąc') 
        matrix = matrix.reindex(index=years, columns=range(1, 13)) # reindeksacja, by mieć pewność, że wszystkie lata i miesiące są obecne
    
        matrix_dict[city] = matrix




    #ustalenie globalnego maksima i minima
    global_min = df_city_month.min().min()
    global_max = df_city_month.max().max()
    
    # Custom mapa kolorów 
    custom_cmap = LinearSegmentedColormap.from_list(
        "PM2.5",
        [
            (0.0,  "green"),   
            (0.15, "yellow"),   
            (0.25, "orange"),  
            (0.40, "red"),  
            (0.60, "black"),     
            (1.00, "purple"),   
        ]
    )
    
    for city in matrix_dict.keys(): 
    
        # ustalamy kształt wykresu 
        fig, ax = plt.subplots(figsize=(12, 4)) 
        
        # ukazanie danych jako obraz, stała mapa kolorów
        im = ax.imshow(matrix_dict[city], aspect='auto', cmap=custom_cmap, vmin=global_min, vmax=global_max) 
        
        # Podpisanie osi wykresu i nazwanie go 
        ax.set_title(f'Średnie miesięczne PM2.5 [µg/m³] w mieście: {city}, w latach: 2015, 2018, 2021, 2024')
        ax.set_xlabel('Miesiąc')
        ax.set_ylabel('Rok')
        
        # upewnienie się że oś x i y będzie wyglądać odpowiednio
        ax.set_xticks(range(12))
        ax.set_xticklabels(range(1, 13))
        ax.set_yticks(range(len(years)))
        ax.set_yticklabels(years)
        
        # colorbar 
        cbar = plt.colorbar(im, ax=ax, label='PM2.5 [µg/m³]')
        
        plt.tight_layout() # żeby uniknąć nakładania się elementów
        
        plt.show()