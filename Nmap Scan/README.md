# 🔍 Network Scanner

Scanner de rede em Python com descoberta de hosts e scan de portas.

---

## 🚀 O que ele faz

- Descobre hosts ativos via ping (ICMP)
- Escaneia portas TCP com `socket`
- Executa em paralelo (multithreading)
- Salva resultados em CSV
- Gera logs do processo

---

## 🧠 Como funciona

1. Você informa:
   - Rede (ex: `192.168.0.0/24`)
   - Portas (ex: `22,80,443`)

2. Para cada IP:
   - Faz ping
   - Se responder → escaneia portas
   - Se não responder → ignora

---

## 📄 Saída

Arquivo: `scan_YYYYMMDD_HHMMSS.csv`

```
origem,destino,22,80,443
192.168.1.5,192.168.1.10,ABERTA,FECHADA,ABERTA
```

Arquivo: `scan.log`

```
2026-03-25 15:00:01 | INFO | 192.168.1.10 respondeu ao PING
2026-03-25 15:00:01 | INFO | 192.168.1.10:22 -> ABERTA
```

---

## ▶️ Como executar

```bash
python scanner.py
```

---

## ⚙️ Configuração

```python
TIMEOUT = 1
MAX_THREADS = 100
```

---

## ⚠️ Observações

- Hosts podem não responder ao ping (firewall)
- Usa TCP Connect (mais detectável)
- Multithreading aumenta performance, mas pode gerar carga na rede

---

## 🔐 Uso

Utilize apenas em redes autorizadas.