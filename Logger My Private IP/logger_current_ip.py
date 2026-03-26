import psutil
import ipaddress
import time
import logging

# -----------------------------
# Configuração do logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | Interface: %(message)s",
    handlers=[
        logging.FileHandler("ip_monitor.log"),
        logging.StreamHandler()
    ]
)

OUTPUT_FILE = "ips_privados.txt"
INTERVALO = 5  # segundos


# -----------------------------
# Função para verificar IP privado
# -----------------------------
def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


# -----------------------------
# Coleta IPs das interfaces
# -----------------------------
def coletar_ips():
    resultado = []

    interfaces = psutil.net_if_addrs()

    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family.name == 'AF_INET':  # IPv4
                ip = addr.address

                if is_private_ip(ip):
                    resultado.append({
                        "interface": interface,
                        "ip": ip
                    })

                    logging.info(f"{interface} | {ip}")

    return resultado


# -----------------------------
# Salva no arquivo
# -----------------------------
def salvar_ips(lista_ips):
    with open(OUTPUT_FILE, "w") as f:
        for item in lista_ips:
            f.write(f"{item['interface']} - {item['ip']}\n")


# -----------------------------
# Loop principal
# -----------------------------
def main():
    while True:
        ips = coletar_ips()
        salvar_ips(ips)
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()