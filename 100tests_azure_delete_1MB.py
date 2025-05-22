# Script qui mesure et enregistre le temps nécessaire pour supprimer un blob de 1 MB
# dans un conteneur Azure Blob Storage, en réuploadant le blob avant chaque suppression pour répéter l’opération 100 fois :

import subprocess
import time
import csv

# Configuration de la connexion Azure
az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
account_name = "stockfabs"
account_key = ""_account_key_""
container_name = "fabiasch"
blob_name = "fichier_1MB.txt"
local_file = "fichier_1MB.txt"
output_csv = "azure_delete_1MB_100x.csv"

# Upload initial pour que le blob existe
print("Upload initial du blob pour démarrer les suppressions...")
init_upload = subprocess.run([
    az_path,
    "storage", "blob", "upload",
    "--account-name", account_name,
    "--account-key", account_key,
    "--container-name", container_name,
    "--name", blob_name,
    "--file", local_file,
    "--overwrite"
])
if init_upload.returncode != 0:
    print("Échec de l'upload initial. Abandon.")
    exit(1)

# Début des tests
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"])

    for i in range(1, 101):
        # Réupload avant chaque suppression
        subprocess.run([
            az_path,
            "storage", "blob", "upload",
            "--account-name", account_name,
            "--account-key", account_key,
            "--container-name", container_name,
            "--name", blob_name,
            "--file", local_file,
            "--overwrite"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Delete {i}/100...")
        start = time.time() # Démarrage du chronomètre

        result = subprocess.run([
            az_path,
            "storage", "blob", "delete",
            "--account-name", account_name,
            "--account-key", account_key,
            "--container-name", container_name,
            "--name", blob_name
        ], capture_output=True, text=True)

        end = time.time() # Fin du chronomètre
        duration = round(end - start, 4) # (Durée arrondie à 4 décimales)
        writer.writerow([i, duration]) # Écriture de l'itération et de la durée

        if result.returncode != 0:
            print(f"Erreur à la suppression {i} : {result.stderr}")
        else:
            print(f"Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")

