import pandas as pd
from pathlib import Path

carpeta = Path(__file__).parent
fitxer = carpeta / "ecv_visualitzacio_final.csv"

df = pd.read_csv(fitxer)

df["rao_no_millora"] = df["rao_no_millora"].map({1: "Falta d’interès", 2: "És massa car", 3: "Dificultat per trobar professionals", 4: "Problemes administratius", 5: "Altres raons"})

if "pes_llar" not in df.columns:
    df["pes_llar"] = 1

sortida = carpeta / "taules_visualitzacio"
sortida.mkdir(exist_ok=True)

def percentatge_ponderat(data, columna, valor):
    data = data[data[columna].notna()].copy()
    if data.empty:
        return 0
    total_pes = data["pes_llar"].sum()
    pes_valor = data.loc[data[columna] == valor, "pes_llar"].sum()
    return round((pes_valor / total_pes) * 100, 2)

def mitjana_ponderada(data, columna):
    data = data[data[columna].notna()].copy()
    if data.empty:
        return None
    return round((data[columna] * data["pes_llar"]).sum() / data["pes_llar"].sum(), 2)

# Indicadors generals
indicadors = pd.DataFrame([
    {"indicador": "Llars en risc de pobresa", "percentatge": percentatge_ponderat(df, "risc_pobresa", "Sí")},
    {"indicador": "Llars amb carència material severa", "percentatge": percentatge_ponderat(df, "carencia_material", "Sí")},
    {"indicador": "Llars sense temperatura adequada", "percentatge": percentatge_ponderat(df, "temperatura_adequada", "No")},
    {"indicador": "Llars amb retards en factures", "percentatge": percentatge_ponderat(df, "retards_factures", "Sí")},
    {"indicador": "Llars amb bo social energètic", "percentatge": percentatge_ponderat(df, "bo_social", "Sí")},
    {"indicador": "Llars amb vulnerabilitat bàsica", "percentatge": percentatge_ponderat(df, "vulnerabilitat_basica", 1)}
])

indicadors.to_csv(sortida / "01_indicadors_generals.csv", index=False, encoding="utf-8-sig")

# Temperatura adequada segons risc de pobresa
files = []

for grup, dades in df.groupby("risc_pobresa"):
    files.append({
        "risc_pobresa": grup,
        "percent_sense_temperatura_adequada": percentatge_ponderat(dades, "no_temperatura_adequada", 1),
        "n_llars": len(dades)
    })

temperatura_pobresa = pd.DataFrame(files)
temperatura_pobresa.to_csv(sortida / "02_temperatura_pobresa.csv", index=False, encoding="utf-8-sig")

# Retards segons capacitat d'arribar a final de mes - format lollipop
ordre_final_mes = ["Amb molta dificultat", "Amb dificultat", "Amb certa dificultat", "Amb certa facilitat", "Amb facilitat", "Amb molta facilitat"]

files_resum = []

for grup, dades in df.groupby("arribar_final_mes"):
    files_resum.append({
        "arribar_final_mes": grup,
        "percent_amb_retards": percentatge_ponderat(dades, "te_retards", 1),
        "n_llars": len(dades)
    })

retards_resum = pd.DataFrame(files_resum)
retards_resum["arribar_final_mes"] = pd.Categorical(retards_resum["arribar_final_mes"], categories=ordre_final_mes, ordered=True)
retards_resum = retards_resum.sort_values("arribar_final_mes")

files_lollipop = []

for _, row in retards_resum.iterrows():
    categoria = row["arribar_final_mes"]
    valor = row["percent_amb_retards"]
    n_llars = row["n_llars"]

    files_lollipop.append({
        "arribar_final_mes": categoria,
        "x": 0,
        "size": 0,
        "percent_amb_retards": valor,
        "n_llars": n_llars
    })

    files_lollipop.append({
        "arribar_final_mes": categoria,
        "x": valor,
        "size": 100,
        "percent_amb_retards": valor,
        "n_llars": n_llars
    })

retards_final_mes = pd.DataFrame(files_lollipop)
retards_final_mes.to_csv(sortida / "03_retards_final_mes.csv", index=False, encoding="utf-8-sig")

# Despeses d'habitatge segons règim de tinença
files = []

for grup, dades in df.groupby("regim_tinenca"):
    files.append({
        "regim_tinenca": grup,
        "mediana_despeses": round(dades["despeses_habitatge"].median(), 2),
        "mitjana_ponderada_despeses": mitjana_ponderada(dades, "despeses_habitatge"),
        "n_llars": len(dades)
    })

despeses_regim = pd.DataFrame(files).sort_values("mediana_despeses", ascending=False)
despeses_regim.to_csv(sortida / "04_despeses_regim_tinenca.csv", index=False, encoding="utf-8-sig")

# Vulnerabilitat bàsica segons règim de tinença
files = []

for grup, dades in df.groupby("regim_tinenca"):
    files.append({
        "regim_tinenca": grup,
        "percent_vulnerabilitat_basica": percentatge_ponderat(dades, "vulnerabilitat_basica", 1),
        "n_llars": len(dades)
    })

vulnerabilitat_regim = pd.DataFrame(files).sort_values("percent_vulnerabilitat_basica", ascending=False)
vulnerabilitat_regim.to_csv(sortida / "05_vulnerabilitat_regim_tinenca.csv", index=False, encoding="utf-8-sig")

# Barreres per no millorar l'eficiencia energetica
barreres = df[df["rao_no_millora"].notna()].copy()

if not barreres.empty:
    files = []
    total_pes = barreres["pes_llar"].sum()

    for codi, dades in barreres.groupby("rao_no_millora"):
        files.append({
            "rao_no_millora": codi,
            "percentatge": round((dades["pes_llar"].sum() / total_pes) * 100, 2),
            "n_llars": len(dades)
        })

    barreres_df = pd.DataFrame(files).sort_values("percentatge", ascending=False)
    barreres_df.to_csv(sortida / "06_barreres_eficiencia.csv", index=False, encoding="utf-8-sig")

print("Taules creades correctament a la carpeta:")
print(sortida)

print("\nFitxers generats:")
for f in sorted(sortida.glob("*.csv")):
    print("-", f.name)