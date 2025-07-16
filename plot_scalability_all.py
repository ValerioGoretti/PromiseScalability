import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# Nomi delle cartelle per ciascun log
log_folders = {
    "BPIC12": "./bpic12Ram",
    "BPIC13": "./bpic13Ram",
    "Sepsis": "./sepsisRam",
}

# Nomi dei file da leggere in ciascuna cartella
csv_files = [
    "scalability_10.csv",
    "scalability_20.csv",
    "scalability_30.csv",
    "scalability_40.csv",
    "scalability_50.csv",
    "scalability_60.csv",
    "scalability_70.csv",
    "scalability_80.csv",
    "scalability_90.csv",
    "scalability_100.csv",
]

# Colori per ciascun log nel plot
log_colors = {
    "BPIC12": "blue",
    "BPIC13": "green",
    "Sepsis": "red",
}

# Dizionario per contenere i dati RAM medi per ogni log
log_ram_data = {}

for log_name, folder in log_folders.items():
    ram_per_num_users = defaultdict(list)

    for filename in csv_files:
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            print(f"[WARNING] File mancante: {filepath}")
            continue
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    num_users = int(row["num_users"])
                    ram_avg = row.get("ram_avg_bytes", "").strip()
                    if ram_avg:
                        #ram_avg = float(ram_avg)
                        ram_avg = float(ram_avg) / 1024
                        ram_per_num_users[num_users].append(ram_avg)
                except Exception as e:
                    print(f"Errore nella riga {row}: {e}")

    # Calcola media RAM per ogni numero di utenti
    average_ram = {
        num_users: sum(values) / len(values) if values else 0
        for num_users, values in ram_per_num_users.items()
    }

    # Salva risultati ordinati
    sorted_x = sorted(average_ram.keys())
    sorted_y = [average_ram[x] for x in sorted_x]
    log_ram_data[log_name] = (sorted_x, sorted_y)

# === PLOT ===
plt.figure(figsize=(10, 6))

for log_name, (x_vals, y_vals) in log_ram_data.items():
    plt.plot(x_vals, y_vals, marker='o', linewidth=2, markersize=6,
             label=log_name, color=log_colors.get(log_name, None))

plt.xlabel("Number of concurrent users")
plt.ylabel("Average RAM usage (KB)")
plt.grid(True, alpha=0.3)
plt.xticks(sorted(x_vals))
plt.legend()
plt.tight_layout()

# Salva e mostra il grafico
plt.savefig("combined_ram_usage.png", dpi=300, bbox_inches='tight')
plt.show()
