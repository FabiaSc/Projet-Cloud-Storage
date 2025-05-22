# Script qui mesure et enregistre le temps nécessaire pour supprimer un fichier de 1MB
# sur un bucket AWS S3, en réuploadant le fichier avant chaque suppression pour répéter l’opération 100 fois :

import subprocess
import time
import csv

bucket = "tests-aws3" # Nom du Bucket utilisé pour les tests
blob_name = "test_auto_delete_1MB.txt" # Nom du fichier à supprimer
output_csv = "aws_delete_1MB_100x.csv" # Fichier CSV où seront stockées les mesures

# Avant les tests, on s'assure que le fichier est bien présent dans le bucket
print("Upload initial du fichier à supprimer 100 fois...")
upload = subprocess.run([
    "aws", "s3", "cp", "fichier_1MB.txt", f"s3://{bucket}/{blob_name}"
])
if upload.returncode != 0:
    print("Erreur lors de l'upload initial. Abandon.")
    exit(1)

# Ouverture/création du fichier CSV pour stocker les résultats
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Iteration", "Duration_seconds"]) # (En-têtes : itération & durée en secondes)

    for i in range(1, 101):
        # Réupload du fichier avant chaque delete pour que l'objet existe
        subprocess.run([
            "aws", "s3", "cp", "fichier_1MB.txt", f"s3://{bucket}/{blob_name}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Delete {i}/100...")
        start = time.time()

        # Suppression de l'objet S3 et capture éventuelle des erreurs
        result = subprocess.run([
            "aws", "s3", "rm", f"s3://{bucket}/{blob_name}"
        ], capture_output=True, text=True)

        end = time.time() # Fin de la mesure
        duration = round(end - start, 4)

        # Ecriture de la durée et de l'itération dans le CSV
        writer.writerow([i, duration])

        if result.returncode != 0:
            print(f"Erreur à la suppression {i} : {result.stderr}")
        else:
            print(f"Durée : {duration}s")

# Fin des tests (indication fichier de résultats)
print(f"\n Résultats enregistrés dans {output_csv}")

