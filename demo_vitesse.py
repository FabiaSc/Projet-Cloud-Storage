import matplotlib.pyplot as plt
import time
import numpy as np

# Données mesurées par région (durées en secondes)
raw_durations_by_region = {
    "AWS - default": {1: 3.34, 10: 5.17, 100: 10.48},
    "AWS - eastasia": {1: 11.17, 10: 27.26, 100: 159.31},
    "Azure - default": {1: 3.82, 10: 5.93, 100: 19.73},
    "Azure - eastasia": {1: 16.78, 10: 19.43, 100: 151.80}
}

# Tailles de fichiers pour lesquelles on veut interpoler les durées (pour une animation fluide)
sizes = [1, 2, 5, 10, 20, 50, 100]

# Interpolation des durées
interpolated_durations = {}
for label, values in raw_durations_by_region.items():
    known_sizes = list(values.keys())   # Tailles connue (1MB, 10MB, 100MB)
    known_durations = list(values.values()) # Durées associées
    interpolated = np.interp(sizes, known_sizes, known_durations) # Interpolation linéaire
    interpolated_durations[label] = interpolated

# Couleurs
colors = {
    "AWS - default": "darkorange",
    "AWS - eastasia": "indianred",
    "Azure - default": "royalblue",
    "Azure - eastasia": "seagreen"
}

# Initialisation des index de progression pour chaque service
progress_index = {label: 0 for label in interpolated_durations}
elapsed_time = 0
last_display_time = {label: 0 for label in interpolated_durations}
# Listes pour stocker les points affichés dynamiquement
displayed_sizes = {label: [] for label in interpolated_durations}
displayed_speeds = {label: [] for label in interpolated_durations}
# Temps auquel chaque service pourra afficher le prochain point
next_ready_time = {
    label: interpolated_durations[label][0] for label in interpolated_durations
}
# Dictionnaire pour retrouver la taille de fichier correspondant à un index
size_lookup = {i: s for i, s in enumerate(sizes)}

# Plot
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6))
lines = {label: ax.plot([], [], label=label, color=colors[label], marker="o")[0]
         for label in interpolated_durations}

ax.set_xlim(0, 110)
ax.set_ylim(0, 12)
ax.set_xlabel("Taille du fichier (MB)")
ax.set_ylabel("Vitesse de transfert (MB/s)")
ax.set_title("Course prioritaire : chaque cloud progresse selon sa vitesse")
ax.grid(True)
ax.legend()
plt.tight_layout()

# Début de la boucle temps réel
start_time = time.time()
active_labels = set(interpolated_durations.keys())

while active_labels:
    elapsed_time = time.time() - start_time # Temps écoulé depuis le début
    for label in list(active_labels):
        idx = progress_index[label] # Position actuelle dans la liste des tailles
        
        #  Si c'est le moment d'afficher un nouveau point pour ce label
        if idx < len(sizes) and elapsed_time >= next_ready_time[label]: 
            size = size_lookup[idx] #  taille de fichier en cours
            duration = interpolated_durations[label][idx] # Durée pour cette taille
            speed = round(size / duration, 2)
            
            # Mise à jour des données affichées
            displayed_sizes[label].append(size)
            displayed_speeds[label].append(speed)
            lines[label].set_data(displayed_sizes[label], displayed_speeds[label])

            # Passage au point suivant
            progress_index[label] += 1
            if progress_index[label] < len(sizes):
                # Planifie le moment d'affichage du prochain point 
                next_ready_time[label] = next_ready_time[label] + interpolated_durations[label][progress_index[label]]
            else:
                active_labels.remove(label)
    # Mise à jour de l'échelle Y si nécessaire pour s'adapter à la vitesse max
    max_y = max([max(v) if v else 0 for v in displayed_speeds.values()] + [10])
    ax.set_ylim(0, max_y + 2)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)

plt.ioff()
plt.show()
