#Création de plot pour comparer les opérations exécutées en Asie
import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

# On charge tous les fichiers CSV dans un DataFrame
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

# Permet de fusionner tous les tableaux
combined_df = pd.concat(dataframes, ignore_index=True)

# Créer le résumé des moyennes par groupe
summary = (
    combined_df
    .groupby(["cloud", "operation", "size", "region"])
    .agg(mean_duration=("Duration_seconds", "mean"), std_duration=("Duration_seconds", "std"))
    .reset_index()
)

# Filtre uniquement les tests en eastasia avec taille 1MB
eastasia_df = summary[
    (summary["region"] == "eastasia") &
    (summary["size"] == "1MB")
]

# Tracer le barplot
plt.figure(figsize=(10, 6))
for operation in ["upload", "download", "delete"]:
    subset = eastasia_df[eastasia_df["operation"] == operation]
    plt.bar(
        subset["cloud"] + f" ({operation})",
        subset["mean_duration"],
        label=operation
    )

plt.title("Comparaison des durées moyennes (1MB - région eastasia)")
plt.ylabel("Durée moyenne (secondes)")
plt.grid(True, axis="y")
plt.tight_layout()
plt.show()



