import pandas as pd
import os

# =========================
# CONFIGURACIÓN
# =========================

INPUT_PATH = "data/processed/historical_index.csv"
OUTPUT_PATH = "data/processed/historical_risk_index.csv"

# Dirección del riesgo por indicador
RISK_DIRECTION = {
    'inflation': True,
    'external_debt': True,
    'current_account': False,
    'gdp_growth': False,
    'reserves_months': False
}

# =========================
# FUNCIONES
# =========================

def load_data(path):
    df = pd.read_csv(path)
    return df

def calculate_historical_index(df, risk_direction):
    all_years = df['year'].unique()
    results = []

    for year in all_years:
        df_year = df[df['year'] == year].pivot(index='country', columns='indicator', values='value')
        df_norm = pd.DataFrame(index=df_year.index)

        for col in df_year.columns:
            col_min, col_max = df_year[col].min(), df_year[col].max()
            if risk_direction.get(col, True):
                df_norm[col] = (df_year[col] - col_min) / (col_max - col_min)
            else:
                df_norm[col] = (col_max - df_year[col]) / (col_max - col_min)
        
        # Calcular score de riesgo compuesto
        df_norm['risk_score'] = df_norm.mean(axis=1) * 100
        df_norm['year'] = year  # Guardar el año correctamente
        df_norm.reset_index(inplace=True)

        results.append(df_norm[['year', 'country', 'risk_score']])  # Guardar correctamente

    df_historical = pd.concat(results, ignore_index=True)
    return df_historical

def save_result(df_final, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False)
    print(f"Índice histórico guardado en {output_path}")

# =========================
# EJECUCIÓN
# =========================

def main():
    df = load_data(INPUT_PATH)
    df_historical = calculate_historical_index(df, RISK_DIRECTION)
    save_result(df_historical, OUTPUT_PATH)

if __name__ == "__main__":
    main()
