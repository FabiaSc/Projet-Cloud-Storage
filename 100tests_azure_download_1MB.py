# Script qui mesure et enregistre le temps nécessaire pour télécharger un blob de 1 MB
# depuis un conteneur Azure Blob Storage, en répétant l’opération 100 fois et en mesurant la durée de chaque téléchargement

import subprocess
import time
import csv
import os

# # Configuration de la connexion Azure
az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
account_name = "stockfabs"
account_key = "_account_key_"
container_name = "fabiasch"
blob_name = "fichier_1MB.txt"  # Nom exact du blob existant sur Azure
output_csv = "azure_download_1MB_100x.csv"

# Lancement des tests
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"]) # (Colonnes : numéro d'itération et durée)

    # Boucle pour répéter le téléchargement 100 fois
    for i in range(1, 101):
        # Nom du fichier local de destination pour cette itération
        local_filename = f"downloaded_1MB_{i}.txt"
        print(f"Download {i}/100...")

        start = time.time() # Démarrage du chronomètre

        # Exécution de la commande Azure CLI pour télécharger le blob
        result = subprocess.run([
            az_path,
            "storage", "blob", "download",
            "--account-name", account_name,
            "--account-key", account_key,
            "--container-name", container_name,
            "--name", blob_name,
            "--file", local_filename,
            "--overwrite"
        ], capture_output=True, text=True)

        end = time.time() # Arrêt du chronomètre
        duration = round(end - start, 4) # Calcul de la durée et arrondi à 4 décimales

        writer.writerow([i, duration]) # Enregistrement des résultats dans le CSV

        if result.returncode != 0:
            print(f"Erreur au téléchargement {i} : {result.stderr}")
        else:
            print(f"Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")
