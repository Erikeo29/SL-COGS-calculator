# Methodologie de calcul COGS

Ce document detaille les formules utilisees par le simulateur.

---

## 1. Parametres globaux

| Parametre | Symbole | Description |
|-----------|---------|-------------|
| Volume annuel | $V$ | Nombre d'unites finies a produire |
| Nombre d'etapes | $N$ | Etapes sequentielles de fabrication |

---

## 2. Parametres par etape $i$

### 2.1 Process (OEE)

| Parametre | Symbole | Unite |
|-----------|---------|-------|
| UPH nominal | $UPH_i$ | unites/heure |
| Disponibilite | $A_i$ | % (0-100) |
| Performance | $P_i$ | % (0-100) |
| Rendement (yield) | $Y_i$ | % (0-100) |

L'**UPH effectif** combine les trois premiers :
$$UPH_{eff,i} = UPH_i \times A_i \times P_i$$

L'**OEE** (Overall Equipment Effectiveness) est :
$$OEE_i = A_i \times P_i \times Y_i$$

### 2.2 Main d'oeuvre directe (DL)

| Parametre | Symbole | Unite |
|-----------|---------|-------|
| Nombre d'operateurs | $n_{ops,i}$ | - |
| Taux horaire | $r_{DL,i}$ | devise/heure |

$$DL_i = \frac{n_{ops,i} \times r_{DL,i}}{UPH_{eff,i}}$$

### 2.3 Frais generaux variables (VOH)

| Parametre | Symbole | Unite |
|-----------|---------|-------|
| Taux VOH | $r_{VOH,i}$ | devise/heure |

$$VOH_i = \frac{r_{VOH,i}}{UPH_{eff,i}}$$

### 2.4 Frais generaux fixes (FOH)

| Parametre | Symbole | Unite |
|-----------|---------|-------|
| FOH total | $FOH_{total,i}$ | devise/an |

$$FOH_i = \frac{FOH_{total,i}}{V}$$

### 2.5 Matieres premieres (BOM)

Pour chaque composant $j$ de l'etape $i$ :

| Parametre | Symbole | Unite |
|-----------|---------|-------|
| Quantite par unite | $q_j$ | - |
| Prix unitaire | $p_j$ | devise |
| Taux de rebut | $s_j$ | % (0-100) |

$$Material_i = \sum_j \frac{q_j \times p_j}{1 - s_j}$$

> **Note** : la division par $(1 - s_j)$ compense les pertes materieres.
> Si 5% du composant est perdu (scrap), il faut en acheter $\frac{1}{0.95} = 1.053\times$ plus.

---

## 3. Cout ajoute par etape

$$CostAdded_i = Material_i + DL_i + VOH_i + FOH_i$$

---

## 4. Cout en cascade (yielded cost)

Le cout cumule apres l'etape $i$ integre les pertes de rendement :

$$YieldedCost_i = \frac{YieldedCost_{i-1} + CostAdded_i}{Y_i}$$

avec $YieldedCost_0 = 0$.

> **Interpretation** : si le rendement d'une etape est 95%, le cout de chaque unite
> "bonne" est divise par 0.95, car 5% des unites sont perdues apres avoir consomme
> des ressources.

---

## 5. Metriques finales

### RTY (Rolled Throughput Yield)
$$RTY = \prod_{i=1}^{N} Y_i$$

### Unites a lancer
$$UnitsToStart = \frac{V}{RTY}$$

### Cout du rebut par unite
$$ScrapCost = YieldedCost_N - \sum_{i=1}^{N} CostAdded_i$$

### COGS total
$$COGS_{total} = YieldedCost_N \times V$$

---

## 6. Analyse de sensibilite

L'analyse de sensibilite evalue l'impact de chaque parametre sur le COGS/unite final.

Pour chaque parametre $p$ :
1. Calcul du COGS avec $p_{base} \times (1 + \delta)$ ($\delta = +10\%$)
2. Calcul du COGS avec $p_{base} \times (1 - \delta)$ ($\delta = -10\%$)
3. Impact = $COGS_{high} - COGS_{low}$

Les parametres sont classes par impact decroissant (tornado chart).

---

## 7. Calculateur prix/marge

### Marge vers prix
$$Prix = \frac{COGS}{1 - Marge\%}$$

### Prix vers marge
$$Marge\% = \frac{Prix - COGS}{Prix} \times 100$$
