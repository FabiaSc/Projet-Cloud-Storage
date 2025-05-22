# Script qui mesure et enregistre le temps nécessaire pour télécharger un fichier de 1 MB
# depuis un bucket AWS S3, en répétant l’opération 100 fois et en sauvegardant la durée de chaque téléchargement

import subprocess
import time
import csv
import os

bucket = "tests-aws3" # Nom du bucket S3 de destination
blob_name = "fichier_1MB.txt" # Nom de l'objet à télécharger depuis le bucket
output_csv = "aws_download_1MB_100x.csv" # Fichier CSV pour stocker les mesures

# Création et ouverture du fichier CSV pour l’écriture des résultats
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"]) # (En-tête : numéro d'itération & durée du téléchargement)

    # Boucle de 1 à 100 pour répéter le test de téléchargement
    for i in range(1, 101):
        # Nom du fichier local qui recevra le blob téléchargé
        local_file = f"downloaded_1MB_{i}.txt"
        print(f"Download {i}/100...") # Affichage de la progression

        start = time.time() # Démarrage du chronomètre

        # Exécution de la commande AWS CLI pour télécharger l'objet depuis S3
        result = subprocess.run([
            "aws", "s3", "cp", f"s3://{bucket}/{blob_name}", local_file
        ], capture_output=True, text=True)

        end = time.time() # Arrêt du chronomètre
        duration = round(end - start, 4) # Calcul de la durée et arrondi à 4 décimales

        writer.writerow([i, duration]) # Enregistrement de l'itération et de la durée dans le CSV

        # Vérification du succès de la commande et affichage du résultat
        if result.returncode != 0:
            print(f" Erreur au download {i} : {result.stderr}")
        else:
            print(f" Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")

