# 📡 SNMP Switch Collector

Script em Python para coleta de informações de switches via SNMP (BULK-WALK).

---

## 🚀 O que ele faz

- Realiza SNMP WALK em múltiplas MIBs
- Coleta informações de interfaces (IF-MIB)
- Mapeia MAC Address por porta (Bridge MIB)
- Traduz status das portas (UP/DOWN)
- Executa coleta em paralelo (threads)
- Exibe resultado organizado por porta

---

## 🧠 Como funciona

Para cada switch:

1. Coleta via SNMP:
   - Nome da interface (ifDescr)
   - Status administrativo (ifAdminStatus)
   - Status operacional (ifOperStatus)
   - Descrição (ifAlias)
   - Tabela MAC Address

2. Correlaciona:
   - Bridge Port → ifIndex
   - MAC → Porta física

3. Monta uma visão final:

```
Porta Gi0/1
  Status Administrativo: UP
  Status Operacional:    UP
  Descrição: Uplink Core
  MACs conectados:
     aa:bb:cc:dd:ee:ff
```

---

## ▶️ Como executar

```bash
python snmp_collector.py
```

---

## ⚙️ Configuração

Defina os switches no código:

```python
switches = [
    ("192.168.10.10", "community"),
]
```

Threads:

```python
for _ in range(6):
```

---

## 📦 Dependência

```bash
pip install pysnmp
```

---

## ⚠️ Observações

- SNMP usa UDP 161
- Community precisa estar liberada no equipamento
- Alguns switches podem limitar BULK-WALK

---

## 🔐 Uso

Utilize apenas em dispositivos autorizados.