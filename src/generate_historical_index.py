import pandas as pd
import os

# ===========================
# Configuración
# ===========================
INPUT_PATH = "data/processed/world_bank_indicators.csv"
OUTPUT_PATH = "data/processed/historical_index.csv"

# Países seleccionados
selected_countries = ["Brazil", "Colombia", "Mexico", "Peru"]

# ===========================
# Función para generar el histórico
# ===========================
def generate_historical_index():
    # Cargar datos
    df = pd.read_csv(INPUT_PATH)
    
    # Filtrar solo países seleccionados
    df = df[df['country'].isin(selected_countries)]
    
    # Asegurar que solo tengamos las columnas necesarias
    df = df[['year', 'country', 'indicator', 'value']].dropna()

    # Guardar el archivo histórico
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Archivo histórico guardado en {OUTPUT_PATH}")

# ===========================
# Ejecución directa
# ===========================
if __name__ == "__main__":
    generate_historical_index()
