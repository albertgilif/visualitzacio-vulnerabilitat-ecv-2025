import pandas as pd
from pathlib import Path

carpeta = Path(__file__).parent
fitxer = carpeta / "ECV_Th_2025.tab"

df = pd.read_csv(fitxer, sep="\t")

cols = [
    "HB030", "HB050", "HB120", "HX060", "HX240", "HY020", "vhRentaa",
    "vhPobreza", "vhMATDEP", "HH021", "HH050", "HH070",
    "cuotahip", "HS011", "HS021", "HS022", "HS060",
    "HS120", "HC006", "HC003A", "HEE07"
]

df = df[cols].copy()

df = df.rename(columns={
    "HB030": "id_llar",
    "HB120": "membres_llar",
    "HX060": "tipus_llar",
    "HX240": "unitats_consum",
    "HY020": "renda_total",
    "vhRentaa": "renda_pobresa",
    "vhPobreza": "risc_pobresa",
    "vhMATDEP": "carencia_material",
    "HH021": "regim_tinenca",
    "HH050": "temperatura_adequada",
    "HH070": "despeses_habitatge",
    "cuotahip": "quota_hipotecaria",
    "HS011": "retards_hipoteca_lloguer",
    "HS021": "retards_factures",
    "HS022": "bo_social",
    "HS060": "afrontar_imprevistos",
    "HS120": "arribar_final_mes",
    "HC006": "any_construccio",
    "HC003A": "millores_energetiques",
    "HEE07": "rao_no_millora",
    "HB050": "pes_llar"
})

df["risc_pobresa"] = df["risc_pobresa"].map({1: "Sí", 0: "No"})
df["carencia_material"] = df["carencia_material"].map({1: "Sí", 0: "No"})
df["temperatura_adequada"] = df["temperatura_adequada"].map({1: "Sí", 2: "No"})
df["bo_social"] = df["bo_social"].map({1: "Sí", 2: "No"})
df["afrontar_imprevistos"] = df["afrontar_imprevistos"].map({1: "Sí", 2: "No"})
df["retards_hipoteca_lloguer"] = df["retards_hipoteca_lloguer"].map({1: "Sí", 2: "Sí", 3: "No"})
df["retards_factures"] = df["retards_factures"].map({1: "Sí", 2: "Sí", 3: "No"})
df["regim_tinenca"] = df["regim_tinenca"].map({1: "Propietat sense hipoteca", 2: "Propietat amb hipoteca", 3: "Lloguer a preu de mercat", 4: "Lloguer inferior al mercat", 5: "Cessió gratuïta"})
df["arribar_final_mes"] = df["arribar_final_mes"].map({1: "Amb molta dificultat", 2: "Amb dificultat", 3: "Amb certa dificultat", 4: "Amb certa facilitat", 5: "Amb facilitat", 6: "Amb molta facilitat"})

df["no_temperatura_adequada"] = df["temperatura_adequada"].map({"Sí": 0, "No": 1})

df["te_retards"] = ((df["retards_hipoteca_lloguer"] == "Sí") | (df["retards_factures"] == "Sí")).astype(int)

df["vulnerabilitat_basica"] = ((df["risc_pobresa"] == "Sí") | (df["carencia_material"] == "Sí") | (df["no_temperatura_adequada"] == 1) | (df["te_retards"] == 1)).astype(int)

sortida = carpeta / "ecv_visualitzacio_final.csv"
df.to_csv(sortida, index=False, encoding="utf-8-sig")

print("Fitxer creat correctament:")
print(sortida)
print("Files i columnes finals:", df.shape)
print(df.head())