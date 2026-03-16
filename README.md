# WiFi MAC Similarity Detector

Este projeto implementa um **detector de dispositivos fora do padrão (outliers)** em uma rede WiFi simulada utilizando **similaridade de conjuntos de MAC addresses**.

A ideia principal é identificar dispositivos que **veem um conjunto de MACs muito diferente dos demais dispositivos do mesmo local**.

Isso pode indicar:

- Pontes de rede não autorizadas
- L2VPN escondida
- Hotspots ou repetidores
- Dispositivos conectados a outra rede

---

# Como o detector funciona

O sistema lê continuamente um arquivo contendo **escaneamentos de MACs WiFi** feitos por vários dispositivos.

Cada linha representa um dispositivo observando MACs próximos.

Formato do arquivo:

```
LOCAL DEVICE MAC1 MAC2 MAC3 MAC4 ...
```

Exemplo:

```
LOCAL1 PC1 AA:11:BB:22:CC:33 12:34:56:78:9A:BC
LOCAL1 PC2 AA:11:BB:22:CC:33 98:76:54:32:10:FF
LOCAL1 PC3 7F:23:11:AA:44:99 8A:33:77:12:BB:CC
```

Onde:

- **LOCAL** → local físico ou rede
- **DEVICE** → dispositivo que fez o scan
- **MACs** → redes WiFi detectadas

---

# Estrutura do sistema

O sistema é dividido em duas threads principais.

## 1️⃣ Leitura do arquivo

Thread responsável por:

- Ler o arquivo `scans_wifi.txt`
- Extrair `local`, `device` e `macs`
- Enviar os dados para uma fila de processamento

Isso permite simular **dados chegando continuamente**.

---

## 2️⃣ Detector de similaridade

Essa thread processa os dados recebidos e executa os seguintes passos:

### Agrupamento por local

Dispositivos são agrupados por local:

```
devices = {
  LOCAL1: {
    PC1: {MACs},
    PC2: {MACs},
    PC3: {MACs}
  }
}
```

---

### Criação de MinHash

Para cada dispositivo é criado um **MinHash**.

MinHash é um algoritmo probabilístico que permite estimar a **similaridade entre conjuntos grandes** de forma eficiente.

Ele reduz o conjunto de MACs para uma **assinatura compacta**.

---

### Cálculo da similaridade

A similaridade entre dois dispositivos é calculada usando **Jaccard Similarity**:

```
similaridade = interseção(MACs) / união(MACs)
```

Valores possíveis:

```
1.0 -> conjuntos idênticos
0.5 -> metade dos MACs iguais
0.0 -> completamente diferentes
```

---

### Similaridade média

Para cada dispositivo, calcula-se a média da similaridade com todos os outros dispositivos do mesmo local.

Exemplo:

```
PC1: 0.82
PC2: 0.79
PC3: 0.05
```

---

### Detecção do outlier

O dispositivo com **menor similaridade média** é considerado o **outlier**.

```
OUTLIER = dispositivo com menor similaridade
```

Exemplo de saída:

```
===================
LOCAL: LOCAL1
-------------------
PC1: 0.82
PC2: 0.79
PC3: 0.05

OUTLIER: PC3
```

---

# Por que isso funciona

Em uma rede normal:

- Dispositivos próximos **veem praticamente os mesmos MACs WiFi**
- A similaridade entre eles é **alta**

Se um dispositivo:

- está conectado a outra rede
- está usando um repetidor
- está atravessando uma VPN bridge

então ele verá **MACs diferentes**, reduzindo drasticamente a similaridade.

---

# Aplicações

Este detector pode ser usado para:

- Detectar **L2VPN escondida**
- Identificar **repetidores WiFi não autorizados**
- Encontrar **pontos de acesso ilegítimos**
- Monitorar **anomalias de rede**

---

# Dependências

Bibliotecas necessárias:

```
datasketch
numpy
```

Instalação:

```
pip install datasketch numpy
```

---

# Arquivos do projeto

```
detect.py        -> detector de similaridade
generator.py     -> gerador de dataset
scans_wifi.txt   -> dados de entrada
```

---

# Fluxo completo

```
Generator -> scans_wifi.txt -> File Reader -> Detector -> Outlier
```

---

# Melhorias futuras

Possíveis evoluções do projeto:

- Janela deslizante temporal de MACs
- Detecção multi-local
- Uso de LSH para escalabilidade
- Dashboard de visualização
- Integração com sistemas de monitoramento de rede

---

# Autor Hugo

Projeto desenvolvido para estudo de **detecção de anomalias em redes WiFi utilizando similaridade de conjuntos**.