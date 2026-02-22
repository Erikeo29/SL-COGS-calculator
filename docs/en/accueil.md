# COGS manufacturing calculator

Welcome to the **interactive COGS simulator** (Cost of Goods Sold) for manufactured products.

---

## What is COGS?

COGS (Cost of Goods Sold) represents the **total manufacturing cost** of a product.
It includes:
- **Materials**: components, sub-assemblies, consumables
- **Direct Labor** (DL): line operators
- **Variable Overhead** (VOH): energy, maintenance, machine consumables
- **Fixed Overhead** (FOH): depreciation, rent, supervision
- **Yield losses** (Scrap): cost of rejected units at each step

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-step simulator** | Model N sequential steps with BOM, process and costs |
| **Cascade calculation** | Each step's yield impacts cumulative cost |
| **Sensitivity analysis** | Identify most impactful parameters (tornado chart) |
| **What-if scenarios** | Compare up to 3 scenarios vs baseline |
| **Price and margin** | Bidirectional calculator margin → price or price → margin |
| **Bilingual FR/EN** | Fully translated interface |

---

## Quick start

1. **Load an example**: click "Load example" in the sidebar
2. **Explore the simulator**: navigate to the "COGS Simulator" page
3. **Modify parameters**: adjust volumes, yields, BOM in real time
4. **Analyze**: review charts and step-by-step detail table

---

## Calculation model

The simulator uses a **multi-step cascade model** where each step's cost
is "loaded" by its yield losses:

$$\text{Yielded Cost}_i = \frac{\text{Yielded Cost}_{i-1} + \text{Cost Added}_i}{\text{Yield}_i}$$

The **RTY** (Rolled Throughput Yield) is the product of all yields:
$$RTY = \prod_{i=1}^{N} \text{Yield}_i$$

---

## Technical stack

| Component | Technology |
|-----------|------------|
| Frontend | [Streamlit](https://streamlit.io) |
| Charts | [Plotly](https://plotly.com) |
| Computation | [NumPy](https://numpy.org), [Pandas](https://pandas.pydata.org) |
| Authentication | [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) |
| Deployment | Streamlit Community Cloud |

---

## License

Internal use only.
