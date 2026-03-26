import threading
import time
from queue import Queue
from datasketch import MinHash
import numpy as np

file_path = "scans_wifi.txt"
data_queue = Queue()

devices = {}

MAC_TIMEOUT = 60  # segundos que o MAC fica na base


# ------------------------
# Thread leitura arquivo
# ------------------------

def file_reader():

    while True:

        try:
            with open(file_path) as f:

                for line in f:

                    parts = line.strip().split()

                    if len(parts) < 3:
                        continue

                    local = parts[0]
                    device = parts[1]
                    macs = set(parts[2:])

                    data_queue.put((local, device, macs))

        except Exception as e:
            print("Erro lendo arquivo:", e)

        time.sleep(5)


# ------------------------
# Thread detector
# ------------------------

def detector():

    while True:

        while not data_queue.empty():

            local, device, macs = data_queue.get()
            now = time.time()

            if local not in devices:
                devices[local] = {}

            if device not in devices[local]:
                devices[local][device] = {}

            # atualiza timestamp dos macs
            for mac in macs:
                devices[local][device][mac] = now


        # limpa MACs expirados
        now = time.time()

        for local in list(devices.keys()):
            for device in list(devices[local].keys()):

                mac_dict = devices[local][device]

                for mac in list(mac_dict.keys()):
                    if now - mac_dict[mac] > MAC_TIMEOUT:
                        del mac_dict[mac]

                # remove device vazio
                if not mac_dict:
                    del devices[local][device]

            # remove local vazio
            if not devices[local]:
                del devices[local]

        # análise
        for local in devices:

            local_devices = devices[local]

            if len(local_devices) < 3:
                continue

            minhashes = {}

            for device, mac_dict in local_devices.items():

                m = MinHash(num_perm=128)

                for mac in mac_dict.keys():
                    m.update(mac.encode())

                minhashes[device] = m


            similarity = {}

            for d1 in local_devices:

                sims = []

                for d2 in local_devices:

                    if d1 == d2:
                        continue

                    sim = minhashes[d1].jaccard(minhashes[d2])
                    sims.append(sim)

                similarity[d1] = np.mean(sims)


            outlier = min(similarity, key=similarity.get)

            print("\n===================")
            print("LOCAL:", local)
            print("-------------------")

            for d, v in similarity.items():
                print(f"{d}: {v:.2f}")

            print("OUTLIER:", outlier)

        time.sleep(5)


# ------------------------
# Inicialização threads
# ------------------------

t1 = threading.Thread(target=file_reader, daemon=True)
t2 = threading.Thread(target=detector, daemon=True)

t1.start()
t2.start()

while True:
    time.sleep(1)