import requests
import time
import concurrent.futures
import csv
import os

# URL del server Go locale (eseguito sulla stessa macchina)
URL = "http://127.0.0.1:8080/process"

# Corpo della richiesta
BODY = {
    "config_id": "01",
    "user_id": "agenas",
    "location": "es",
    "algorithm": "HeuristicMiner",
    "techniqueType": "AutomatedDiscovery"
}

# Lista di test: numero di utenti simultanei
CONCURRENT_USERS_LIST = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Funzione per inviare una richiesta e misurare i timestamp
def send_request(user_index, num_users):
    start_time = time.time()
    try:
        response = requests.post(URL, json=BODY, timeout=300)
        end_time = time.time()
        return (num_users, user_index, start_time, end_time)
    except Exception as e:
        print(f"Errore nella richiesta dell'utente {user_index}: {e}")
        return (num_users, user_index, start_time, None)

# Esecuzione test
for num_users in CONCURRENT_USERS_LIST:
    output_file = f"scalability_{num_users}.csv"
    print(f"\n[INFO] Simulazione con {num_users} utenti simultanei. Salvataggio in: {output_file}")

    # Pausa di 5 secondi tra i test
    time.sleep(5)

    # Esegue tutte le richieste concorrenti
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(send_request, i + 1, num_users) for i in range(num_users)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # Scrive i risultati nel file CSV corrispondente
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["num_users", "user_id", "start_time", "end_time"])
        for result in results:
            writer.writerow(result)
