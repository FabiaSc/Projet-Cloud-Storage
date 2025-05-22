#Calcule de l'écart-type pour les opérations localisées en Asie
import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

# Charger tous les fichiers CSV disponibles 
csv_files = glob("*.csv")

dataframes = []
for filepath in csv_files:
    filename = os.path.basename(filepath).replace(".csv", "")
    parts = filename.split("_")
    
    if len(parts) < 4:
        continue

    cloud = "azure" if "azure" in parts[0] else "aws"
    operation = parts[1]
    size = parts[2]
    region = "eastasia" if "eastasia" in filename else "default"

    df = pd.read_csv(filepath)
    df["cloud"] = cloud
    df["operation"] = operation
    df["size"] = size
    df["region"] = region
    dataframes.append(df)

# On fusionne tous les tableaux
combined_df = pd.concat(dataframes, ignore_index=True)

# Résumé par groupe
summary = (
    combined_df
    .groupby(["cloud", "operation", "size", "region"])
    .agg(mean_duration=("Duration_seconds", "mean"), std_duration=("Duration_seconds", "std"))
    .reset_index()
)

# Garder uniquement les 1MB eastasia
eastasia_df = summary[
    (summary["region"] == "eastasia") &
    (summary["size"] == "1MB")
]

# Tableau croisé
pivot_df = eastasia_df.pivot(index="operation", columns="cloud", values="mean_duration")

# Calcul de l'écart relatif en %
pivot_df["écart_%"] = ((pivot_df["azure"] - pivot_df["aws"]) / pivot_df["aws"]) * 100

# Tracer le plot
plt.figure(figsize=(8, 5))
pivot_df["écart_%"].sort_values().plot(kind="barh", color="crimson")
plt.title("Écart de performance Azure vs AWS (1MB - eastasia)")
plt.xlabel("Écart de durée (%)")
plt.axvline(0, color="black", linewidth=0.8)
plt.grid(True, axis="x")
plt.tight_layout()
plt.show()

