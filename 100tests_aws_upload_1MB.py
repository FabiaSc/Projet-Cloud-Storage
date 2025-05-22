# Script qui mesure et enregistre le temps nécessaire pour uploader un fichier de 1 MB
# sur un bucket AWS S3, en répétant l’opération 100 fois et en enregistrant la durée de chaque upload

import subprocess
import time
import csv

fichier_local = "fichier_1MB.txt" # Chemin local vers le fichier à uploader
bucket = "tests-aws3" # Nom du bucket S3 de destination
blob_name = "test_auto_upload_1MB.txt" # Nom de l'objet créé dans le bucket

output_csv = "aws_upload_1MB_100x.csv" # Fichier CSV de sortie


# Ouverture du fichier CSV et écriture de l'en-tête
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"]) # (Colonnes : itération & durée en secondes)

    # Boucle pour répéter l'upoad 100x
    for i in range(1, 101):
        print(f"Upload {i}/100...")
        start = time.time()

        # Exécution de la commande AWS CLI pour uploader le fichier
        result = subprocess.run([
            "aws", "s3", "cp", fichier_local, f"s3://{bucket}/{blob_name}"
        ], capture_output=True, text=True)

        end = time.time() # Arrêt du chronomètre
        duration = round(end - start, 4) # Calcul de la durée et arrondi à 4 décimales

        writer.writerow([i, duration]) # Enregistrment des résultats dans le CSV

        # Vérification du succès de la commande et affichage du résultat
        if result.returncode != 0:
            print(f"Erreur à l'upload {i} : {result.stderr}")
        else:
            print(f"Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")

