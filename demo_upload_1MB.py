import matplotlib.pyplot as plt
import time

# Configuration
n = 50 # Nombre total de fichiers à uploader
durations = {
    "AWS - default": 3.34,
    "AWS - eastasia": 11.17,
    "Azure - default": 3.82,
    "Azure - eastasia": 16.78
}
colors = {
    "AWS - default": "darkorange",
    "AWS - eastasia": "indianred",
    "Azure - default": "royalblue",
    "Azure - eastasia": "seagreen"
}

# Initialisation pour stocker les points de progression
progress = {k: [] for k in durations} # Nombre de fichiers uploadés dans le temps
times = {k: [] for k in durations} # Temps auquel chaque fichier a été uploadé
counters = {k: 0 for k in durations} # Compteur de fichiers uploadés pour chaque Cloud
next_upload = {k: durations[k] for k in durations} # Prochaine échéance d'upload pour 

# Plot interactif
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6))
lines = {}


for label in durations:
    lines[label], = ax.plot([], [], label=label, color=colors[label], marker='o')

ax.set_xlim(0, n * max(durations.values()) + 5) # Axe X : temps estimé maximal
ax.set_ylim(0, n + 1) # Axe Y : nombre de fichiers uploadés
ax.set_xlabel("Temps écoulé (secondes)")
ax.set_ylabel("Nombre de fichiers uploadés")
ax.set_title("Simulation en temps réel : Upload 1MB (Azure vs AWS, default & eastasia)")
ax.grid(True)
ax.legend()
plt.tight_layout()

# Simulation temps réel par incrément
current_time = 0 # Temps écoulé depuis le début de la simulation
time_step = 0.5  # Incrément de temps simulé à chaque boucle

# Continue tant qu'au moins un cloud upload 50 fichiers
while any(counters[k] < n for k in durations):
    for label in durations:
        if counters[label] < n and current_time >= next_upload[label]:
            counters[label] += 1
            times[label].append(current_time)
            progress[label].append(counters[label])
            next_upload[label] += durations[label]
            lines[label].set_data(times[label], progress[label])

    ax.set_xlim(0, current_time + 5)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(time_step)
    current_time += time_step

plt.ioff()
plt.show()
