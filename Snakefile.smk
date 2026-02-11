import yaml
from pathlib import Path

# wczytanie konfiguracji
CONFIG = "config/task4.yaml"
cfg = yaml.safe_load(open(CONFIG))

YEARS = cfg.get("years", [])

# --- LISTY PLIKÓW (Bez zmian) ---
PM25_FILES = [f"results/pm25/{y}/data/monthly_means.csv" for y in YEARS] + \
             [f"results/pm25/{y}/data/daily_means.csv" for y in YEARS] + \
             [f"results/pm25/{y}/data/exceedance_days.csv" for y in YEARS]

PM25_PLOTS = [f"results/pm25/{y}/figures/pm25_mean_plot.png" for y in YEARS] + \
             [f"results/pm25/{y}/figures/pm25_heatmap.png" for y in YEARS] + \
             [f"results/pm25/{y}/figures/pm25_grouped_barplot.png" for y in YEARS]

PUBMED_FILES = [f"results/literature/{y}/pubmed_results.csv" for y in YEARS] + \
               [f"results/literature/{y}/top_journals.csv" for y in YEARS] + \
               [f"results/literature/{y}/summary_by_year.csv" for y in YEARS]

REPORT_FILES = ["results/report_task4.md", "results/publication_trends.png"]

rule all:
    input:
        PM25_FILES + PM25_PLOTS + PUBMED_FILES + REPORT_FILES

rule pm25_year:
    """Generuje wyniki PM2.5 dla pojedynczego roku."""
    # USUNIĘTO: input: config = CONFIG (to psuło inkrementalność)
    output:
        data_monthly = "results/pm25/{year}/data/monthly_means.csv",
        data_daily = "results/pm25/{year}/data/daily_means.csv",
        data_exceed = "results/pm25/{year}/data/exceedance_days.csv",
        fig_mean = "results/pm25/{year}/figures/pm25_mean_plot.png",
        fig_heat = "results/pm25/{year}/figures/pm25_heatmap.png",
        fig_bar = "results/pm25/{year}/figures/pm25_grouped_barplot.png",
    params:
        config = CONFIG  # Ścieżka zostaje przekazana do shella
    shell:
        "python src/pm_2_5/pm25.py --year {wildcards.year} --config {params.config}"

rule pubmed_year:
    """Pobiera metadane z PubMed dla pojedynczego roku."""
    # USUNIĘTO: input: config = CONFIG
    output:
        results_dir = "results/literature/{year}/pubmed_results.csv",
        top = "results/literature/{year}/top_journals.csv",
        summary = "results/literature/{year}/summary_by_year.csv",
    params:
        config = CONFIG
    shell:
        "python src/PubMed/pubmed.py --year {wildcards.year} --config {params.config}"

rule report:
    """Generuje raport markdown i wykres trendów."""
    input:
        pm25 = PM25_FILES + PM25_PLOTS,
        pubmed = PUBMED_FILES,
        config = CONFIG # Tutaj ZOSTAWIAMY, bo zmiana listy lat POWINNA wymusić nowy raport!
    output:
        md = REPORT_FILES[0],
        png = REPORT_FILES[1],
    params:
        config = CONFIG,
    shell:
        "python src/report/report.py --config {params.config}"



