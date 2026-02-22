# Calculateur COGS manufacturing

Bienvenue dans le **simulateur interactif de COGS** (Cost of Goods Sold) pour produits manufacturés.

---

## Qu'est-ce que le COGS ?

Le COGS (Cost of Goods Sold) représente le **coût total de fabrication** d'un produit.
Il inclut :
- **Matières premières** : composants, sous-ensembles, consommables
- **Main d'œuvre directe** (DL) : opérateurs sur ligne
- **Frais généraux variables** (VOH) : énergie, maintenance, consommables machine
- **Frais généraux fixes** (FOH) : amortissements, loyer, encadrement
- **Pertes de rendement** (Scrap) : coût des unités rejetées à chaque étape

---

## Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| **Simulateur multi-étapes** | Modéliser N étapes séquentielles avec BOM, process et coûts |
| **Calcul en cascade** | Le rendement de chaque étape impacte le coût cumulé |
| **Analyse de sensibilité** | Identifier les paramètres les plus impactants (tornado chart) |
| **Scénarios what-if** | Comparer jusqu'à 3 scénarios vs la configuration de base |
| **Prix et marge** | Calculateur bidirectionnel marge → prix ou prix → marge |
| **Bilingue FR/EN** | Interface entièrement traduite |

---

## Démarrage rapide

1. **Charger un exemple** : cliquez sur "Charger l'exemple" dans la barre latérale
2. **Explorer le simulateur** : naviguez vers la page "Simulateur COGS"
3. **Modifier les paramètres** : ajustez volumes, rendements, BOM en temps réel
4. **Analyser** : consultez les graphiques et le tableau de détail par étape

---

## Modèle de calcul

Le simulateur utilise un modèle de **cascade multi-étapes** où le coût de chaque étape
est "chargé" par les pertes de rendement (yield) de cette étape :

$$\text{Yielded Cost}_i = \frac{\text{Yielded Cost}_{i-1} + \text{Cost Added}_i}{\text{Yield}_i}$$

Le **RTY** (Rolled Throughput Yield) est le produit de tous les rendements :
$$RTY = \prod_{i=1}^{N} \text{Yield}_i$$

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | [Streamlit](https://streamlit.io) |
| Graphiques | [Plotly](https://plotly.com) |
| Calcul | [NumPy](https://numpy.org), [Pandas](https://pandas.pydata.org) |
| Authentification | [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) |
| Déploiement | Streamlit Community Cloud |

---

## Licence

Usage interne uniquement.
