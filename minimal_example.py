from pysnmp.hlapi import *
from threading import Thread
from queue import Queue


def snmp_walk(host, community, oid):
    """Executa um BULK-WALK e retorna {oid: valor}"""
    resultado = {}

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in bulkCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, 161), timeout=2, retries=1),
            ContextData(),
            0, 25,
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
    ):
        if errorIndication or errorStatus:
            return None

        for oid, value in varBinds:
            resultado[str(oid)] = str(value)

    return resultado


def traduz_status(valor):
    """Tradução para status"""
    if valor == "1":
        return "UP"
    elif valor == "2":
        return "DOWN"
    elif valor == "3":
        return "TESTING"
    return valor


def montar_tabela_amigavel(dados):
    """Monta tabela por porta unificando todas as MIBs"""

    portas = {}

    ifDescr       = dados.get("ifDescr") or {}
    ifAdminStatus = dados.get("ifAdminStatus") or {}
    ifOperStatus  = dados.get("ifOperStatus") or {}
    ifAlias       = dados.get("ifAlias") or {}

    macAddress    = dados.get("macAddress") or {}
    macPort       = dados.get("macPort") or {}
    bridgeIfIndex = dados.get("bridgeIfIndex") or {}

    # Converte: BRIDGE port -> IF-MIB ifIndex
    bridge_map = {}
    for bridge_oid, ifindex in bridgeIfIndex.items():
        # Último número da OID é o bridge port
        bridge_port = bridge_oid.split('.')[-1]
        bridge_map[bridge_port] = ifindex

    # MACs por ifIndex
    mac_por_ifindex = {}

    for oid, mac in macAddress.items():
        mac_num = oid.split('.')[-1]  # index da tabela
        porta_bridge = macPort.get(f"1.3.6.1.2.1.17.4.3.1.2.{mac_num}")

        if not porta_bridge:
            continue

        ifindex = bridge_map.get(porta_bridge)

        if not ifindex:
            continue

        mac_formatado = ":".join(f"{int(x):02x}" for x in mac.split("."))

        if ifindex not in mac_por_ifindex:
            mac_por_ifindex[ifindex] = []

        mac_por_ifindex[ifindex].append(mac_formatado)

    # Monta a tabela de portas
    for oid, nome_porta in ifDescr.items():
        ifindex = oid.split('.')[-1]

        portas[ifindex] = {
            "nome": nome_porta,
            "admin": traduz_status(ifAdminStatus.get(f"1.3.6.1.2.1.2.2.1.7.{ifindex}", "0")),
            "oper": traduz_status(ifOperStatus.get(f"1.3.6.1.2.1.2.2.1.8.{ifindex}", "0")),
            "alias": ifAlias.get(f"1.3.6.1.2.1.31.1.1.1.18.{ifindex}", ""),
            "macs": mac_por_ifindex.get(ifindex, [])
        }

    return portas


def coletar_switch(host, community):
    print(f"[+] Coletando {host}")

    dados = {
        "ifDescr": snmp_walk(host, community, "1.3.6.1.2.1.2.2.1.2"),
        "ifAdminStatus": snmp_walk(host, community, "1.3.6.1.2.1.2.2.1.7"),
        "ifOperStatus": snmp_walk(host, community, "1.3.6.1.2.1.2.2.1.8"),
        "ifAlias": snmp_walk(host, community, "1.3.6.1.2.1.31.1.1.1.18"),

        "macAddress": snmp_walk(host, community, "1.3.6.1.2.1.17.4.3.1.1"),
        "macPort": snmp_walk(host, community, "1.3.6.1.2.1.17.4.3.1.2"),
        "bridgeIfIndex": snmp_walk(host, community, "1.3.6.1.2.1.17.1.4.1.2")
    }

    print(f"[✓] Finalizado {host}\n")

    return montar_tabela_amigavel(dados)


def worker(q, results):
    while not q.empty():
        host, comm = q.get()
        results[host] = coletar_switch(host, comm)
        q.task_done()


def main():
    switches = [
        ("192.168.10.10", "pipoca"),
    ]

    q = Queue()
    results = {}

    for item in switches:
        q.put(item)

    threads = []
    for _ in range(6):
        t = Thread(target=worker, args=(q, results))
        t.start()
        threads.append(t)

    q.join()

    print("===== RESULTADO FINAL =====")
    for host, portas in results.items():
        print(f"\n==== SWITCH {host} ====\n")
        for ifindex, info in portas.items():
            print(f"Porta {info['nome']} (ifIndex {ifindex})")
            print(f"  Status Administrativo: {info['admin']}")
            print(f"  Status Operacional:    {info['oper']}")
            print(f"  Descrição (Alias):     {info['alias']}")

            if info["macs"]:
                print("  MACs conectados:")
                for mac in info["macs"]:
                    print(f"     {mac}")
            else:
                print("  MACs conectados: Nenhum")

            print("")

    return results

def snmp_octetstring_to_mac(val):
    """
    Converte OctetString do PySNMP para MAC no formato xxxx.xxxx.xxxx
    """
    try:
        raw = bytes(val)  # converte OctetString → bytes
        if len(raw) != 6:
            return None

        mac_hex = "".join(f"{b:02x}" for b in raw)
        return f"{mac_hex[0:4]}.{mac_hex[4:8]}.{mac_hex[8:12]}"
    except:
        return None


if __name__ == "__main__":
    # main()
    result = snmp_walk('192.168.10.10', 'pipoca', "1.3.6.1.2.1.17.4.3.1.1")
    print(result)