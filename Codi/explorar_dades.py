import pandas as pd
from pathlib import Path

carpeta = Path(__file__).parent
fitxer = carpeta / "ecv_visualitzacio_final.csv"

df = pd.read_csv(fitxer)

print("Files i columnes:", df.shape)

print("\nRisc de pobresa:")
print(df["risc_pobresa"].value_counts(dropna=False, normalize=True) * 100)

print("\nCarència material:")
print(df["carencia_material"].value_counts(dropna=False, normalize=True) * 100)

print("\nTemperatura adequada:")
print(df["temperatura_adequada"].value_counts(dropna=False, normalize=True) * 100)

print("\nRetards en factures:")
print(df["retards_factures"].value_counts(dropna=False, normalize=True) * 100)

print("\nBo social:")
print(df["bo_social"].value_counts(dropna=False, normalize=True) * 100)

print("\nVulnerabilitat bàsica:")
print(df["vulnerabilitat_basica"].value_counts(dropna=False, normalize=True) * 100)

print("\nTemperatura no adequada segons risc de pobresa:")
print(df.groupby("risc_pobresa")["no_temperatura_adequada"].mean() * 100)

print("\nRetards segons capacitat d'arribar a final de mes:")
print(df.groupby("arribar_final_mes")["te_retards"].mean() * 100)

print("\nMediana de despeses d'habitatge segons règim de tinença:")
print(df.groupby("regim_tinenca")["despeses_habitatge"].median().sort_values(ascending=False))