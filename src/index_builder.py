import pandas as pd
import os

# =========================
# CONFIGURACIÓN
# =========================

INPUT_PATH = "data/processed/base_index.csv"
OUTPUT_PATH = "data/processed/country_risk_score.csv"

# Dirección del riesgo por indicador
# True: a mayor valor, mayor riesgo
# False: a mayor valor, menor riesgo
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

def normalize_indicators(df_base, risk_direction):
    df_wide = df_base.pivot(index='country', columns='indicator', values='value')
    df_norm = pd.DataFrame(index=df_wide.index)

    for col in df_wide.columns:
        col_min, col_max = df_wide[col].min(), df_wide[col].max()
        if col_min == col_max:
            df_norm[col] = 0  # evitar división por cero
        elif risk_direction[col]:
            df_norm[col] = (df_wide[col] - col_min) / (col_max - col_min)
        else:
            df_norm[col] = (col_max - df_wide[col]) / (col_max - col_min)

    return df_norm

def apply_weights(df_norm):
    n = df_norm.shape[1]
    weights = {col: 1 / n for col in df_norm.columns}
    df_norm['risk_score'] = sum(df_norm[col] * w for col, w in weights.items())
    df_norm['risk_score'] *= 100  # escalar a 0–100
    return df_norm.reset_index()

def save_result(df_final, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final[['country', 'risk_score']].to_csv(output_path, index=False)
    print(f"Índice guardado en {output_path}")

# =========================
# EJECUCIÓN
# =========================

def main():
    df_base = load_data(INPUT_PATH)
    df_norm = normalize_indicators(df_base, RISK_DIRECTION)
    df_final = apply_weights(df_norm)
    save_result(df_final, OUTPUT_PATH)

if __name__ == "__main__":
    main()
