# Script qui mesure et enregistre le temps nécessaire pour uploader un fichier de 1 MB
# dans un conteneur Azure Blob Storage, en répétant l’opération 100 fois et en vérifiant la présence du fichier local

import subprocess
import time
import csv

# Configuration de la connexion Azure
az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
account_name = "stockfabs"
account_key = "account_key"
container_name = "fabiasch"
blob_name = "test_auto_upload_1MB.txt"
local_file = "fichier_1MB.txt" # Nom exact du blob existant sur Azure
output_csv = "azure_upload_1MB_100x.csv"

# Vérification du fichier local
print("Vérification que le fichier local existe...")
try:
    open(local_file, "rb").close() # Essaye d'ouvrir le fichier en lecture binaire
except FileNotFoundError:
    print(f"Le fichier '{local_file}' est introuvable.") # Avertit si le fichier manque
    exit(1)

# Lancement des tests
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"]) # (Colonnes : numéro d'itération et durée d'upload)

    # Boucle pour répéter l'upload 100 fois
    for i in range(1, 101):
        print(f"Upload {i}/100...") # Affichage de la progression

        start = time.time() # Démarrage du chronomètre

        # Exécution de la commande Azure CLI pour uploader le blob
        result = subprocess.run([
            az_path,
            "storage", "blob", "upload",
            "--account-name", account_name,
            "--account-key", account_key,
            "--container-name", container_name,
            "--name", blob_name,
            "--file", local_file,
            "--overwrite"
        ], capture_output=True, text=True)

        end = time.time() # Arrêt du chronomètre
        duration = round(end - start, 4) # Calcul de la durée et arrondi à 4 décimales
        writer.writerow([i, duration]) # Enregistrement des résultats dans le CSV

        # Vérification du succès et affichage du résultat
        if result.returncode != 0:
            print(f"Erreur à l'upload {i} : {result.stderr}")
        else:
            print(f"Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")
