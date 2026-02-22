# Calculateur COGS manufacturing

Bienvenue dans le **simulateur interactif de COGS** (Cost of Goods Sold) pour produits manufacturés.

---

## Qu'est-ce que le COGS ?

Le COGS (Cost of Goods Sold) represente le **cout total de fabrication** d'un produit.
Il inclut :
- **Matieres premieres** : composants, sous-ensembles, consommables
- **Main d'oeuvre directe** (DL) : operateurs sur ligne
- **Frais generaux variables** (VOH) : energie, maintenance, consommables machine
- **Frais generaux fixes** (FOH) : amortissements, loyer, encadrement
- **Pertes de rendement** (Scrap) : cout des unites rejetees a chaque etape

---

## Fonctionnalites

| Fonctionnalite | Description |
|----------------|-------------|
| **Simulateur multi-etapes** | Modeliser N etapes sequentielles avec BOM, process et couts |
| **Calcul en cascade** | Le rendement de chaque etape impacte le cout cumule |
| **Analyse de sensibilite** | Identifier les parametres les plus impactants (tornado chart) |
| **Scenarios what-if** | Comparer jusqu'a 3 scenarios vs la configuration de base |
| **Prix et marge** | Calculateur bidirectionnel marge → prix ou prix → marge |
| **Bilingue FR/EN** | Interface entierement traduite |

---

## Demarrage rapide

1. **Charger un exemple** : cliquez sur "Charger l'exemple" dans la barre laterale
2. **Explorer le simulateur** : naviguez vers la page "Simulateur COGS"
3. **Modifier les parametres** : ajustez volumes, rendements, BOM en temps reel
4. **Analyser** : consultez les graphiques et le tableau de detail par etape

---

## Modele de calcul

Le simulateur utilise un modele de **cascade multi-etapes** ou le cout de chaque etape
est "charge" par les pertes de rendement (yield) de cette etape :

$$\text{Yielded Cost}_i = \frac{\text{Yielded Cost}_{i-1} + \text{Cost Added}_i}{\text{Yield}_i}$$

Le **RTY** (Rolled Throughput Yield) est le produit de tous les rendements :
$$RTY = \prod_{i=1}^{N} \text{Yield}_i$$
