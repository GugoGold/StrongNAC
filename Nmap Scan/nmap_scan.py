import socket
import ipaddress
import csv
import logging
import subprocess
import platform
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# -----------------------------
# CONFIG
# -----------------------------
TIMEOUT = 1
MAX_THREADS = 100

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scan.log"),
        logging.StreamHandler()
    ]
)

# -----------------------------
# PING RÁPIDO (ICMP)
# -----------------------------
def ping_host(ip):
    try:
        sistema = platform.system().lower()

        if sistema == "windows":
            comando = ["ping", "-n", "1", "-w", "500", str(ip)]
        else:
            comando = ["ping", "-c", "1", "-W", "1", str(ip)]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if resultado.returncode == 0:
            logging.info(f"{ip} respondeu ao PING")
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Erro no ping {ip}: {e}")
        return False


# -----------------------------
# SCAN PORTA
# -----------------------------
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        result = sock.connect_ex((str(ip), port))

        if result == 0:
            return "ABERTA"
        else:
            return "FECHADA"

    except:
        return "ERRO"

    finally:
        sock.close()


# -----------------------------
# INPUT
# -----------------------------
def obter_rede():
    while True:
        try:
            return ipaddress.ip_network(input("Rede (ex: 192.168.0.0/24): "), strict=False)
        except:
            print("Rede inválida")


def obter_portas():
    while True:
        try:
            return [int(p.strip()) for p in input("Portas (ex: 22,80,443): ").split(",")]
        except:
            print("Entrada inválida")


# -----------------------------
# SCAN DE HOST
# -----------------------------
def scan_host(ip, portas, origem):

    # 🔥 PASSO 1: PING
    if not ping_host(ip):
        logging.info(f"{ip} INATIVO (ignorado)")
        return None  # 🔥 NÃO SALVA

    resultado = {
        "origem": origem,
        "destino": str(ip)
    }

    logging.info(f"{ip} ATIVO -> iniciando scan de portas")

    # 🔥 PASSO 2: SCAN PORTAS
    for porta in portas:
        status = scan_port(ip, porta)
        logging.info(f"{ip}:{porta} -> {status}")
        resultado[str(porta)] = status

    return resultado


# -----------------------------
# EXECUÇÃO PARALELA
# -----------------------------
def executar_scan(rede, portas):
    resultados = []
    origem = socket.gethostbyname(socket.gethostname())

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [
            executor.submit(scan_host, ip, portas, origem)
            for ip in rede.hosts()
        ]

        for future in as_completed(futures):
            resultado = future.result()

            if resultado is not None:  # 🔥 FILTRO FINAL
                resultados.append(resultado)

    return resultados


# -----------------------------
# CSV
# -----------------------------
def salvar_csv(resultados, portas):
    nome = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    campos = ["origem", "destino"] + [str(p) for p in portas]

    with open(nome, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)

    logging.info(f"Resultado salvo em {nome}")


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("==== SCANNER COM PING + THREADS ====")

    rede = obter_rede()
    portas = obter_portas()

    resultados = executar_scan(rede, portas)
    salvar_csv(resultados, portas)


if __name__ == "__main__":
    main()