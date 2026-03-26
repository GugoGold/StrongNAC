import random

arquivo = "scans_wifi.txt"


# ----------------------------
# Gerar MAC address real
# ----------------------------

def gerar_mac():
    return ":".join(f"{random.randint(0,255):02X}" for _ in range(6))


# ----------------------------
# Gerar MACs únicos
# ----------------------------

def gerar_macs(qtd):

    macs = set()

    while len(macs) < qtd:
        macs.add(gerar_mac())

    return list(macs)


# ----------------------------
# Gerar dados simulados
# ----------------------------

def gerar_dataset(locais, pcs_por_local, macs_por_local, gerar_intruso=False):

    linhas = []

    for l in range(1, locais + 1):

        local = f"LOCAL{l}"

        macs_base = gerar_macs(macs_por_local)

        # escolhe qual PC será intruso
        pc_intruso = random.randint(1, pcs_por_local) if gerar_intruso else None

        for p in range(1, pcs_por_local + 1):

            device = f"PC{p}"

            qtd_visivel = random.randint(
                int(macs_por_local * 0.6),
                macs_por_local
            )

            # PC intruso -> MACs totalmente aleatórios
            if p == pc_intruso:

                macs_vistos = gerar_macs(qtd_visivel)

            else:

                macs_vistos = random.sample(macs_base, qtd_visivel)

            linha = f"{local} {device} " + " ".join(macs_vistos)

            linhas.append(linha)

    return linhas


# ----------------------------
# Inputs
# ----------------------------

locais = int(input("Quantidade de locais: "))
pcs = int(input("PCs por local: "))
macs = int(input("MACs base por local: "))
intruso = input("Gerar PC intruso? (s/n): ").lower() == "s"


# ----------------------------
# Gerar dataset
# ----------------------------

linhas = gerar_dataset(locais, pcs, macs, intruso)


# ----------------------------
# Salvar arquivo
# ----------------------------

with open(arquivo, "w") as f:

    for linha in linhas:
        f.write(linha + "\n")


print("\nArquivo gerado:", arquivo)
print("\nPrimeiras linhas:\n")

for l in linhas[:10]:
    print(l)