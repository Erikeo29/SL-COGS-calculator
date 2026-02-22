# Méthodologie de calcul COGS

Ce document détaille les formules utilisées par le simulateur.

---

## 1. Paramètres globaux

| Paramètre | Symbole | Description |
|-----------|---------|-------------|
| Volume annuel | $V$ | Nombre d'unités finies à produire |
| Nombre d'étapes | $N$ | Étapes séquentielles de fabrication |

---

## 2. Paramètres par étape $i$

### 2.1 Process (OEE)

| Paramètre | Symbole | Unité |
|-----------|---------|-------|
| UPH nominal | $UPH_i$ | unités/heure |
| Disponibilité | $A_i$ | % (0-100) |
| Performance | $P_i$ | % (0-100) |
| Rendement (yield) | $Y_i$ | % (0-100) |

L'**UPH effectif** combine les trois premiers :
$$UPH_{eff,i} = UPH_i \times A_i \times P_i$$

L'**OEE** (Overall Equipment Effectiveness) est :
$$OEE_i = A_i \times P_i \times Y_i$$

### 2.2 Main d'œuvre directe (DL)

| Paramètre | Symbole | Unité |
|-----------|---------|-------|
| Nombre d'opérateurs | $n_{ops,i}$ | - |
| Taux horaire | $r_{DL,i}$ | devise/heure |

$$DL_i = \frac{n_{ops,i} \times r_{DL,i}}{UPH_{eff,i}}$$

### 2.3 Frais généraux variables (VOH)

| Paramètre | Symbole | Unité |
|-----------|---------|-------|
| Taux VOH | $r_{VOH,i}$ | devise/heure |

$$VOH_i = \frac{r_{VOH,i}}{UPH_{eff,i}}$$

### 2.4 Frais généraux fixes (FOH)

| Paramètre | Symbole | Unité |
|-----------|---------|-------|
| FOH total | $FOH_{total,i}$ | devise/an |

$$FOH_i = \frac{FOH_{total,i}}{V}$$

### 2.5 Matières premières (BOM)

Pour chaque composant $j$ de l'étape $i$ :

| Paramètre | Symbole | Unité |
|-----------|---------|-------|
| Quantité par unité | $q_j$ | - |
| Prix unitaire | $p_j$ | devise |
| Taux de rebut | $s_j$ | % (0-100) |

$$Material_i = \sum_j \frac{q_j \times p_j}{1 - s_j}$$

> **Note** : la division par $(1 - s_j)$ compense les pertes matières.
> Si 5% du composant est perdu (scrap), il faut en acheter $\frac{1}{0.95} = 1.053\times$ plus.

---

## 3. Coût ajouté par étape

$$CostAdded_i = Material_i + DL_i + VOH_i + FOH_i$$

---

## 4. Coût en cascade (yielded cost)

Le coût cumulé après l'étape $i$ intègre les pertes de rendement :

$$YieldedCost_i = \frac{YieldedCost_{i-1} + CostAdded_i}{Y_i}$$

avec $YieldedCost_0 = 0$.

> **Interprétation** : si le rendement d'une étape est 95%, le coût de chaque unité
> "bonne" est divisé par 0.95, car 5% des unités sont perdues après avoir consommé
> des ressources.

---

## 5. Métriques finales

### RTY (Rolled Throughput Yield)
$$RTY = \prod_{i=1}^{N} Y_i$$

### Unités à lancer
$$UnitsToStart = \frac{V}{RTY}$$

### Coût du rebut par unité
$$ScrapCost = YieldedCost_N - \sum_{i=1}^{N} CostAdded_i$$

### COGS total
$$COGS_{total} = YieldedCost_N \times V$$

---

## 6. Analyse de sensibilité

L'analyse de sensibilité évalue l'impact de chaque paramètre sur le COGS/unité final.

Pour chaque paramètre $p$ :
1. Calcul du COGS avec $p_{base} \times (1 + \delta)$ ($\delta = +10\%$)
2. Calcul du COGS avec $p_{base} \times (1 - \delta)$ ($\delta = -10\%$)
3. Impact = $COGS_{high} - COGS_{low}$

Les paramètres sont classés par impact décroissant (tornado chart).

---

## 7. Calculateur prix/marge

### Marge vers prix
$$Prix = \frac{COGS}{1 - Marge\%}$$

### Prix vers marge
$$Marge\% = \frac{Prix - COGS}{Prix} \times 100$$
