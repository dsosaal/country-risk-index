import os
import pandas as pd
import requests

BASE_URL = "http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000"

# Países seleccionados
countries = {
    "Mexico": "MX",
    "Brazil": "BR",
    "Colombia": "CO",
    "Chile": "CL",
    "Peru": "PE",
    "Argentina": "AR"
}

# Indicadores y sus códigos del World Bank
indicators = {
    "inflation": "FP.CPI.TOTL.ZG",
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",
    "current_account": "BN.CAB.XOKA.GD.ZS",
    "external_debt": "DT.DOD.DECT.GN.ZS",
    "reserves_months": "FI.RES.TOTL.MO"
}

def fetch_indicator_data(country_code, indicator_code):
    url = BASE_URL.format(country=country_code, indicator=indicator_code)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[1]
        return pd.DataFrame(data)
    else:
        print(f"Error al obtener datos: {country_code} - {indicator_code}")
        return pd.DataFrame()

def clean_data(df, country_name, indicator_name):
    if df.empty:
        return df
    df_clean = df[["date", "value"]].copy()
    df_clean["country"] = country_name
    df_clean["indicator"] = indicator_name
    df_clean = df_clean.rename(columns={"date": "year", "value": "value"})
    df_clean = df_clean.dropna()
    return df_clean

def build_dataset():
    all_data = []
    for country_name, country_code in countries.items():
        for indicator_name, indicator_code in indicators.items():
            df_raw = fetch_indicator_data(country_code, indicator_code)
            df_clean = clean_data(df_raw, country_name, indicator_name)
            all_data.append(df_clean)

    final_df = pd.concat(all_data, ignore_index=True)
    os.makedirs("data/processed", exist_ok=True)
    final_df.to_csv("data/processed/world_bank_indicators.csv", index=False)
    print("✅ Datos guardados en data/processed/world_bank_indicators.csv")

if __name__ == "__main__":
    build_dataset()
