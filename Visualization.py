import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math

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


def heatmap(df, years):
    # grupowanie po mieście
    df_city_month = df.groupby(level='Miejscowość', axis=1).mean()
    
    
    matrix_dict = {} # słownik na macierze dla poszczególnych miast
    for city in df_city_month.columns:
        matrix = df_city_month[city].unstack(level='Miesiąc')
        matrix = matrix.reindex(index=years, columns=range(1, 13))  # reindeksacja, by mieć pewność, że wszystkie lata i miesiące są obecne
        matrix_dict[city] = matrix
    
    # ustalenie globalnego maksima i minima
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
    
    cities = list(matrix_dict.keys())
    n_cities = len(cities)
    
    # układ siatki
    ncols = 5
    nrows = math.ceil(n_cities / ncols)
    
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(15, 9),
        constrained_layout=True
    )
    
    axes = axes.flatten()
    
    for i, city in enumerate(cities):
        ax = axes[i]
        im = ax.imshow(
            matrix_dict[city],
            aspect='auto',
            cmap=custom_cmap,
            vmin=global_min,
            vmax=global_max
        )

        # upewnienie się że oś x i y będzie wyglądać odpowiednio
        ax.set_title(city, fontsize=10)
        ax.set_xticks(range(12))
        ax.set_xticklabels(range(1, 13), fontsize=8)
        ax.set_yticks(range(len(years)))
        ax.set_yticklabels(years, fontsize=8)

        # Podpisanie osi wykresu 
        ax.set_xlabel("Miesiąc", fontsize=8)
        ax.set_ylabel("Rok", fontsize=8)
    
    # usunięcie pustych paneli (jeśli < 20 miast)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    
    # wspólna colorbar
    cbar = fig.colorbar(
        im,
        ax=axes,
        orientation="vertical",
        fraction=0.02,
        pad=0.02
    )
    cbar.set_label("PM2.5 [µg/m³]")
    
    # nazwanie wykresu
    fig.suptitle(
        "Średnie miesięczne stężenia PM2.5 w miastach (2015, 2018, 2021, 2024)",
        fontsize=16
    )
    
    plt.show()
