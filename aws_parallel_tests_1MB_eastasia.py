#Lancement de 100 tests parallèles pour AWS localisé en Asie
import subprocess
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config AWS S3 (East Asia via ap-southeast-1)
bucket = "fabia-aws-eastasia"
local_file = "fichier_10MB.txt"

def run_operation(op_type, iteration):
    """Lance upload, download ou delete et retourne la durée."""
    s3_key = f"{op_type}_10MB_{iteration}.txt"
    file = local_file if op_type != "download" else f"dl_10MB_{iteration}.txt"

    # Ici on s'assure que tout est upload avant delete et download
    if op_type in ["download", "delete"]:
        subprocess.run([
            "aws", "s3", "cp", local_file, f"s3://{bucket}/{s3_key}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command = {
        "upload": ["aws", "s3", "cp", local_file, f"s3://{bucket}/{s3_key}"],
        "download": ["aws", "s3", "cp", f"s3://{bucket}/{s3_key}", file],
        "delete": ["aws", "s3", "rm", f"s3://{bucket}/{s3_key}"]
    }[op_type]

    start = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    end = time.time()
    duration = round(end - start, 4)

    return (iteration, duration, result.returncode, result.stderr if result.returncode != 0 else None)

# CSV output files (eastasia-specific) permet de récupérer lees données
outputs = {
    "upload": open("aws_upload_10MB_eastasia.csv", "w", newline=""),
    "download": open("aws_download_10MB_eastasia.csv", "w", newline=""),
    "delete": open("aws_delete_10MB_eastasia.csv", "w", newline="")
}
writers = {key: csv.writer(outputs[key]) for key in outputs}
for w in writers.values():
    w.writerow(["Iteration", "Duration_seconds", "Status", "Error"])

# L'execution des tests en parallèle
with ThreadPoolExecutor(max_workers=12) as executor:
    futures = {}

    for i in range(1, 101):
        for op in ["upload", "download", "delete"]:
            future = executor.submit(run_operation, op, i)
            futures[future] = op

    for future in as_completed(futures):
        op_type = futures[future]
        iteration, duration, code, err = future.result()
        writers[op_type].writerow([iteration, duration, "OK" if code == 0 else "ERROR", err])

# Fermer les fichiers
for f in outputs.values():
    f.close()

print("Tous les tests AWS 10MB eastasia sont terminés.")

