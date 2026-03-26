# 🌐 IP Monitor

Script em Python para monitorar IPs privados das interfaces de rede.

---

## 🚀 O que ele faz

- Lista IPs das interfaces de rede
- Filtra apenas IPs privados
- Atualiza automaticamente a cada 5 segundos
- Salva em arquivo `.txt`
- Gera logs em tempo real

---

## 📄 Saída

Arquivo: `ips_privados.txt`

```
eth0 - 192.168.0.10
wlan0 - 192.168.1.5
```

Arquivo: `ip_monitor.log`

```
2026-03-25 15:00:01 | INFO | Interface: eth0 | 192.168.0.10
```

---

## ▶️ Como executar

```bash
python ip_monitor.py
```

---

## 📦 Dependência

```bash
pip install psutil
```

---

## ⚙️ Configuração

```python
INTERVALO = 5  # tempo entre coletas (segundos)
```

---

## ⚠️ Observação

O arquivo é sobrescrito a cada execução (sempre mostra o estado atual).