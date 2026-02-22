# COGS calculation methodology

This document details the formulas used by the simulator.

---

## 1. Global parameters

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| Annual volume | $V$ | Number of finished units to produce |
| Number of steps | $N$ | Sequential manufacturing steps |

---

## 2. Per-step parameters (step $i$)

### 2.1 Process (OEE)

| Parameter | Symbol | Unit |
|-----------|--------|------|
| Nominal UPH | $UPH_i$ | units/hour |
| Availability | $A_i$ | % (0-100) |
| Performance | $P_i$ | % (0-100) |
| Yield | $Y_i$ | % (0-100) |

**Effective UPH** combines the first three:
$$UPH_{eff,i} = UPH_i \times A_i \times P_i$$

**OEE** (Overall Equipment Effectiveness):
$$OEE_i = A_i \times P_i \times Y_i$$

### 2.2 Direct Labor (DL)

| Parameter | Symbol | Unit |
|-----------|--------|------|
| Number of operators | $n_{ops,i}$ | - |
| Hourly rate | $r_{DL,i}$ | currency/hour |

$$DL_i = \frac{n_{ops,i} \times r_{DL,i}}{UPH_{eff,i}}$$

### 2.3 Variable Overhead (VOH)

| Parameter | Symbol | Unit |
|-----------|--------|------|
| VOH rate | $r_{VOH,i}$ | currency/hour |

$$VOH_i = \frac{r_{VOH,i}}{UPH_{eff,i}}$$

### 2.4 Fixed Overhead (FOH)

| Parameter | Symbol | Unit |
|-----------|--------|------|
| Total FOH | $FOH_{total,i}$ | currency/year |

$$FOH_i = \frac{FOH_{total,i}}{V}$$

### 2.5 Bill of Materials (BOM)

For each component $j$ at step $i$:

| Parameter | Symbol | Unit |
|-----------|--------|------|
| Quantity per unit | $q_j$ | - |
| Unit price | $p_j$ | currency |
| Scrap rate | $s_j$ | % (0-100) |

$$Material_i = \sum_j \frac{q_j \times p_j}{1 - s_j}$$

> **Note**: dividing by $(1 - s_j)$ compensates for material losses.
> If 5% of a component is lost (scrap), you need $\frac{1}{0.95} = 1.053\times$ more.

---

## 3. Cost added per step

$$CostAdded_i = Material_i + DL_i + VOH_i + FOH_i$$

---

## 4. Cascade cost (yielded cost)

Cumulative cost after step $i$ integrates yield losses:

$$YieldedCost_i = \frac{YieldedCost_{i-1} + CostAdded_i}{Y_i}$$

with $YieldedCost_0 = 0$.

> **Interpretation**: if a step's yield is 95%, each "good" unit's cost is
> divided by 0.95, because 5% of units are lost after consuming resources.

---

## 5. Final metrics

### RTY (Rolled Throughput Yield)
$$RTY = \prod_{i=1}^{N} Y_i$$

### Units to start
$$UnitsToStart = \frac{V}{RTY}$$

### Scrap cost per unit
$$ScrapCost = YieldedCost_N - \sum_{i=1}^{N} CostAdded_i$$

### Total COGS
$$COGS_{total} = YieldedCost_N \times V$$

---

## 6. Sensitivity analysis

Sensitivity analysis evaluates each parameter's impact on the final COGS/unit.

For each parameter $p$:
1. Compute COGS with $p_{base} \times (1 + \delta)$ ($\delta = +10\%$)
2. Compute COGS with $p_{base} \times (1 - \delta)$ ($\delta = -10\%$)
3. Impact = $COGS_{high} - COGS_{low}$

Parameters are ranked by decreasing impact (tornado chart).

---

## 7. Price/margin calculator

### Margin to price
$$Price = \frac{COGS}{1 - Margin\%}$$

### Price to margin
$$Margin\% = \frac{Price - COGS}{Price} \times 100$$
