"""COGS Manufacturing Calculator - Streamlit Application."""

import json
import os
from copy import deepcopy

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit_authenticator as stauth
import yaml

# ─── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COGS Calculator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Authentication ─────────────────────────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

with open(CONFIG_PATH) as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login()

if st.session_state.get("authentication_status") is None:
    st.warning("Please enter your credentials.")
    st.stop()
elif st.session_state.get("authentication_status") is False:
    st.error("Username or password incorrect.")
    st.stop()

# ─── Paths & Version ────────────────────────────────────────────────────────────
DOC_PATH = os.path.join(ROOT_DIR, "docs")
DATA_PATH = os.path.join(ROOT_DIR, "data")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")
CSS_PATH = os.path.join(ASSETS_PATH, "style.css")

VERSION = "1.0.1"
VERSION_DATE = "Feb 2026"
VERSION_NOTES = {
    "fr": "Correction typographie FR, bouton retour en haut",
    "en": "FR typography fix, scroll-to-top button",
}

# ─── Color palette ──────────────────────────────────────────────────────────────
COLORS = {
    "material": "#3498db",
    "dl": "#e67e22",
    "voh": "#9b59b6",
    "foh": "#1abc9c",
    "scrap": "#e74c3c",
}

# ─── TRANSLATIONS ───────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "fr": {
        # Sidebar / Nav
        "sidebar_title": "COGS Calculator",
        "nav_header": "Navigation",
        "gen_header": "Général",
        "study_header": "Études",
        "annex_header": "Annexes",
        "gen_pages": ["Accueil", "Simulateur COGS"],
        "study_pages": ["Analyse de sensibilité", "Scénarios what-if"],
        "annex_pages": ["Méthodologie"],
        "lang_fr": "Français",
        "lang_en": "English",
        "load_sample": "Charger l'exemple",
        "load_sample_help": "Capteur électrochimique médical (5 étapes)",
        "version_info": "**Revision {version}** {date}<br>{notes}<br>© Eric QUEAU — Licence MIT",
        # Global params
        "global_params": "Paramètres globaux",
        "volume": "Volume annuel",
        "currency": "Devise",
        "nb_steps": "Nombre d'étapes",
        "step": "Étape",
        # BOM
        "bom_title": "Nomenclature (BOM)",
        "component": "Composant",
        "qty": "Quantité",
        "price": "Prix unitaire",
        "scrap_rate": "Taux de rebut (%)",
        "add_component": "Ajouter composant",
        "remove": "Supprimer",
        # Process
        "process_title": "Process",
        "uph": "UPH nominal",
        "availability": "Disponibilité (%)",
        "performance": "Performance (%)",
        "yield": "Rendement / Yield (%)",
        "effective_uph": "UPH effectif",
        "oee": "OEE",
        # Costs
        "costs_title": "Coûts",
        "nb_operators": "Nombre d'opérateurs",
        "dl_rate": "Taux DL (devise/h)",
        "voh_rate": "Taux VOH (devise/h)",
        "foh_total": "FOH total (devise/an)",
        # Results
        "results_title": "Résultats",
        "cogs_per_unit": "COGS / unité",
        "rty": "RTY",
        "units_to_start": "Unités à lancer",
        "scrap_cost": "Coût rebut / unité",
        "total_cogs": "COGS total",
        "detail_table": "Détail par étape",
        "cost_buildup": "Buildup des coûts par étape",
        "cost_breakdown": "Répartition globale des coûts",
        # Detail table columns
        "col_step": "Étape",
        "col_material": "Matériel",
        "col_dl": "Main d'œuvre (DL)",
        "col_voh": "VOH",
        "col_foh": "FOH",
        "col_cost_added": "Coût ajouté",
        "col_yield": "Yield",
        "col_yielded_cost": "Coût cumulé (yielded)",
        "col_scrap_cost": "Coût rebut",
        # Price / Margin
        "price_margin_title": "Calculateur prix / marge",
        "calc_mode": "Mode de calcul",
        "margin_to_price": "Marge → Prix",
        "price_to_margin": "Prix → Marge",
        "target_margin": "Marge cible (%)",
        "selling_price": "Prix de vente",
        "margin_result": "Marge",
        "price_result": "Prix de vente calculé",
        "unit_profit": "Profit unitaire",
        # Sensitivity
        "sensitivity_title": "Analyse de sensibilité",
        "sensitivity_desc": "Impact d'une variation de ±10% de chaque paramètre sur le COGS/unité.",
        "tornado_title": "Tornado chart - Top 15 paramètres",
        "param_name": "Paramètre",
        "impact": "Impact sur COGS/unité",
        "variation": "Variation",
        # Scenarios
        "scenarios_title": "Scénarios what-if",
        "scenarios_desc": "Comparez jusqu'à 3 scénarios avec la configuration de base.",
        "nb_scenarios": "Nombre de scénarios",
        "scenario": "Scénario",
        "base": "Base",
        "scenario_name": "Nom du scénario",
        "scenario_comparison": "Comparaison des scénarios",
        "scenario_param": "Paramètre à modifier",
        "scenario_step_select": "Étape concernée",
        "scenario_new_value": "Nouvelle valeur",
        "add_modification": "Ajouter une modification",
        "scenario_detail": "Détail du scénario",
        "scenario_delta": "Delta vs base",
        "all_steps": "Toutes les étapes",
        # Misc
        "no_data": "Aucune donnée chargée. Chargez l'exemple depuis la barre latérale.",
        "data_loaded": "Données chargées avec succès !",
        "export_json": "Exporter (JSON)",
        "step_name": "Nom de l'étape",
    },
    "en": {
        # Sidebar / Nav
        "sidebar_title": "COGS Calculator",
        "nav_header": "Navigation",
        "gen_header": "General",
        "study_header": "Studies",
        "annex_header": "Annexes",
        "gen_pages": ["Home", "COGS Simulator"],
        "study_pages": ["Sensitivity analysis", "What-if scenarios"],
        "annex_pages": ["Methodology"],
        "lang_fr": "Francais",
        "lang_en": "English",
        "load_sample": "Load example",
        "load_sample_help": "Electrochemical medical sensor (5 steps)",
        "version_info": "**Revision {version}** {date}<br>{notes}<br>© Eric QUEAU — Licence MIT",
        # Global params
        "global_params": "Global parameters",
        "volume": "Annual volume",
        "currency": "Currency",
        "nb_steps": "Number of steps",
        "step": "Step",
        # BOM
        "bom_title": "Bill of Materials (BOM)",
        "component": "Component",
        "qty": "Quantity",
        "price": "Unit price",
        "scrap_rate": "Scrap rate (%)",
        "add_component": "Add component",
        "remove": "Remove",
        # Process
        "process_title": "Process",
        "uph": "Nominal UPH",
        "availability": "Availability (%)",
        "performance": "Performance (%)",
        "yield": "Yield (%)",
        "effective_uph": "Effective UPH",
        "oee": "OEE",
        # Costs
        "costs_title": "Costs",
        "nb_operators": "Number of operators",
        "dl_rate": "DL rate (currency/h)",
        "voh_rate": "VOH rate (currency/h)",
        "foh_total": "Total FOH (currency/yr)",
        # Results
        "results_title": "Results",
        "cogs_per_unit": "COGS / unit",
        "rty": "RTY",
        "units_to_start": "Units to start",
        "scrap_cost": "Scrap cost / unit",
        "total_cogs": "Total COGS",
        "detail_table": "Step-by-step detail",
        "cost_buildup": "Cost buildup by step",
        "cost_breakdown": "Global cost breakdown",
        # Detail table columns
        "col_step": "Step",
        "col_material": "Material",
        "col_dl": "Direct Labor (DL)",
        "col_voh": "VOH",
        "col_foh": "FOH",
        "col_cost_added": "Cost added",
        "col_yield": "Yield",
        "col_yielded_cost": "Yielded cost (cumul.)",
        "col_scrap_cost": "Scrap cost",
        # Price / Margin
        "price_margin_title": "Price / margin calculator",
        "calc_mode": "Calculation mode",
        "margin_to_price": "Margin → Price",
        "price_to_margin": "Price → Margin",
        "target_margin": "Target margin (%)",
        "selling_price": "Selling price",
        "margin_result": "Margin",
        "price_result": "Calculated selling price",
        "unit_profit": "Unit profit",
        # Sensitivity
        "sensitivity_title": "Sensitivity analysis",
        "sensitivity_desc": "Impact of a ±10% variation of each parameter on COGS/unit.",
        "tornado_title": "Tornado chart - Top 15 parameters",
        "param_name": "Parameter",
        "impact": "Impact on COGS/unit",
        "variation": "Variation",
        # Scenarios
        "scenarios_title": "What-if scenarios",
        "scenarios_desc": "Compare up to 3 scenarios with the baseline configuration.",
        "nb_scenarios": "Number of scenarios",
        "scenario": "Scenario",
        "base": "Baseline",
        "scenario_name": "Scenario name",
        "scenario_comparison": "Scenario comparison",
        "scenario_param": "Parameter to modify",
        "scenario_step_select": "Target step",
        "scenario_new_value": "New value",
        "add_modification": "Add modification",
        "scenario_detail": "Scenario detail",
        "scenario_delta": "Delta vs baseline",
        "all_steps": "All steps",
        # Misc
        "no_data": "No data loaded. Load the example from the sidebar.",
        "data_loaded": "Data loaded successfully!",
        "export_json": "Export (JSON)",
        "step_name": "Step name",
    },
}


# ─── Helper functions ────────────────────────────────────────────────────────────
def t(key: str) -> str:
    """Return translation for current language."""
    lang = st.session_state.get("lang", "fr")
    return TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)


@st.cache_data(ttl=3600)
def load_custom_css(path: str) -> str:
    """Load CSS file content."""
    with open(path) as f:
        return f.read()


@st.cache_data(ttl=600)
def load_file_content(path: str) -> str:
    """Load markdown file content."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_sample_data() -> dict:
    """Load sample medical device JSON."""
    path = os.path.join(DATA_PATH, "sample_medical_device.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_step_name(step_data: dict) -> str:
    """Get step name in current language."""
    lang = st.session_state.get("lang", "fr")
    name = step_data.get("name", {})
    if isinstance(name, dict):
        return name.get(lang, name.get("fr", f"Step"))
    return str(name)


def get_component_name(comp: dict) -> str:
    """Get component name in current language."""
    lang = st.session_state.get("lang", "fr")
    name = comp.get("name", {})
    if isinstance(name, dict):
        return name.get(lang, name.get("fr", "Component"))
    return str(name)


def sample_to_session(sample: dict) -> None:
    """Convert sample JSON to session state format."""
    st.session_state.volume = sample.get("volume", 100000)
    st.session_state.currency = sample.get("currency", "EUR")
    steps = sample.get("steps", [])
    st.session_state.nb_steps = len(steps)
    st.session_state.steps_data = []
    for step in steps:
        step_entry = {
            "name": step.get("name", {"fr": "Étape", "en": "Step"}),
            "uph": step.get("uph", 60),
            "availability": step.get("availability", 0.90),
            "performance": step.get("performance", 0.85),
            "yield": step.get("yield", 0.95),
            "nb_operators": step.get("nb_operators", 1),
            "dl_rate": step.get("dl_rate", 25.0),
            "voh_rate": step.get("voh_rate", 30.0),
            "foh_total": step.get("foh_total", 50000),
            "bom": step.get("bom", []),
        }
        st.session_state.steps_data.append(step_entry)


def session_to_json() -> str:
    """Export current session state to JSON string."""
    lang = st.session_state.get("lang", "fr")
    data = {
        "name": {"fr": "Export", "en": "Export"},
        "volume": st.session_state.get("volume", 100000),
        "currency": st.session_state.get("currency", "EUR"),
        "steps": st.session_state.get("steps_data", []),
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


# ─── COGS Calculation Engine ────────────────────────────────────────────────────
def compute_cogs(steps_data: list, volume: int) -> dict:
    """Compute COGS for all steps using cascade model.

    Returns dict with per-step results and global metrics.
    """
    results = []
    yielded_cost = 0.0
    rty = 1.0

    for i, step in enumerate(steps_data):
        uph = step.get("uph", 60)
        avail = step.get("availability", 0.90)
        perf = step.get("performance", 0.85)
        yld = step.get("yield", 0.95)

        effective_uph = uph * avail * perf
        oee = avail * perf * yld

        # Direct Labor
        nb_ops = step.get("nb_operators", 1)
        dl_rate = step.get("dl_rate", 25.0)
        dl_per_unit = (nb_ops * dl_rate / effective_uph) if effective_uph > 0 else 0

        # Variable Overhead
        voh_rate = step.get("voh_rate", 30.0)
        voh_per_unit = (voh_rate / effective_uph) if effective_uph > 0 else 0

        # Fixed Overhead
        foh_total = step.get("foh_total", 50000)
        foh_per_unit = (foh_total / volume) if volume > 0 else 0

        # Material (BOM)
        material_per_unit = 0.0
        bom = step.get("bom", [])
        for comp in bom:
            qty = comp.get("qty", 1)
            price = comp.get("price", 0)
            scrap = comp.get("scrap", 0)
            denom = 1 - scrap
            if denom > 0:
                material_per_unit += qty * price / denom
            else:
                material_per_unit += qty * price

        cost_added = material_per_unit + dl_per_unit + voh_per_unit + foh_per_unit

        # Yielded cost (cascade)
        if yld > 0:
            yielded_cost = (yielded_cost + cost_added) / yld
        else:
            yielded_cost = yielded_cost + cost_added

        rty *= yld

        # Scrap cost for this step
        scrap_cost_step = (yielded_cost - (yielded_cost * yld + cost_added * (1 - yld))) \
            if yld < 1 else 0
        # Simpler: scrap cost = yielded_cost - (prev_yielded + cost_added)
        # = (prev + cost_added)/yld - prev - cost_added
        # = (prev + cost_added) * (1/yld - 1)
        prev_yielded = yielded_cost * yld - cost_added  # reconstruct
        scrap_cost_step = (prev_yielded + cost_added) * (1.0 / yld - 1.0) if yld > 0 and yld < 1 else 0

        results.append({
            "step_idx": i,
            "name": get_step_name(step),
            "uph": uph,
            "effective_uph": round(effective_uph, 1),
            "oee": round(oee * 100, 1),
            "material": round(material_per_unit, 4),
            "dl": round(dl_per_unit, 4),
            "voh": round(voh_per_unit, 4),
            "foh": round(foh_per_unit, 4),
            "cost_added": round(cost_added, 4),
            "yield": yld,
            "yielded_cost": round(yielded_cost, 4),
            "scrap_cost": round(scrap_cost_step, 4),
        })

    units_to_start = volume / rty if rty > 0 else volume
    total_cost_added = sum(r["cost_added"] for r in results)
    total_scrap_cost = round(yielded_cost - total_cost_added, 4) if results else 0

    return {
        "steps": results,
        "cogs_per_unit": round(yielded_cost, 4),
        "rty": round(rty, 4),
        "units_to_start": round(units_to_start, 0),
        "scrap_cost_per_unit": total_scrap_cost,
        "total_cogs": round(yielded_cost * volume, 2),
    }


# ─── Sensitivity Analysis Engine ────────────────────────────────────────────────
def run_sensitivity(steps_data: list, volume: int, delta: float = 0.10) -> list:
    """Run sensitivity analysis on all parameters.

    Returns list of {param_name, base_value, impact_high, impact_low, impact}.
    """
    base_result = compute_cogs(steps_data, volume)
    base_cogs = base_result["cogs_per_unit"]
    impacts = []

    # Volume
    for direction, mult in [("high", 1 + delta), ("low", 1 - delta)]:
        new_vol = max(1, int(volume * mult))
        r = compute_cogs(steps_data, new_vol)
        if direction == "high":
            cogs_high = r["cogs_per_unit"]
        else:
            cogs_low = r["cogs_per_unit"]
    impacts.append({
        "param": t("volume"),
        "step": "-",
        "impact_high": round(cogs_high - base_cogs, 4),
        "impact_low": round(cogs_low - base_cogs, 4),
        "impact": round(abs(cogs_high - cogs_low), 4),
    })

    # Per-step parameters
    param_keys = [
        ("uph", t("uph")),
        ("availability", t("availability")),
        ("performance", t("performance")),
        ("yield", t("yield")),
        ("nb_operators", t("nb_operators")),
        ("dl_rate", t("dl_rate")),
        ("voh_rate", t("voh_rate")),
        ("foh_total", t("foh_total")),
    ]

    for step_idx, step in enumerate(steps_data):
        step_name = get_step_name(step)
        for key, label in param_keys:
            base_val = step.get(key, 0)
            if base_val == 0:
                continue

            cogs_high = base_cogs
            cogs_low = base_cogs

            for direction, mult in [("high", 1 + delta), ("low", 1 - delta)]:
                modified = deepcopy(steps_data)
                new_val = base_val * mult
                # Clamp percentages
                if key in ("availability", "performance", "yield"):
                    new_val = min(new_val, 1.0)
                modified[step_idx][key] = new_val
                r = compute_cogs(modified, volume)
                if direction == "high":
                    cogs_high = r["cogs_per_unit"]
                else:
                    cogs_low = r["cogs_per_unit"]

            impacts.append({
                "param": f"{step_name} - {label}",
                "step": step_name,
                "impact_high": round(cogs_high - base_cogs, 4),
                "impact_low": round(cogs_low - base_cogs, 4),
                "impact": round(abs(cogs_high - cogs_low), 4),
            })

    # BOM components
    for step_idx, step in enumerate(steps_data):
        step_name = get_step_name(step)
        for comp_idx, comp in enumerate(step.get("bom", [])):
            comp_name = get_component_name(comp)
            base_price = comp.get("price", 0)
            if base_price == 0:
                continue

            cogs_high = base_cogs
            cogs_low = base_cogs

            for direction, mult in [("high", 1 + delta), ("low", 1 - delta)]:
                modified = deepcopy(steps_data)
                modified[step_idx]["bom"][comp_idx]["price"] = base_price * mult
                r = compute_cogs(modified, volume)
                if direction == "high":
                    cogs_high = r["cogs_per_unit"]
                else:
                    cogs_low = r["cogs_per_unit"]

            impacts.append({
                "param": f"{step_name} - {comp_name} ({t('price')})",
                "step": step_name,
                "impact_high": round(cogs_high - base_cogs, 4),
                "impact_low": round(cogs_low - base_cogs, 4),
                "impact": round(abs(cogs_high - cogs_low), 4),
            })

    impacts.sort(key=lambda x: x["impact"], reverse=True)
    return impacts


# ─── Chart builders ──────────────────────────────────────────────────────────────
def build_waterfall_chart(results: dict) -> go.Figure:
    """Build stacked bar chart showing cost buildup per step."""
    steps = results["steps"]
    step_names = [s["name"] for s in steps]

    fig = go.Figure()
    for cat, key, color in [
        (t("col_material"), "material", COLORS["material"]),
        (t("col_dl"), "dl", COLORS["dl"]),
        ("VOH", "voh", COLORS["voh"]),
        ("FOH", "foh", COLORS["foh"]),
        (t("scrap_cost"), "scrap_cost", COLORS["scrap"]),
    ]:
        fig.add_trace(go.Bar(
            name=cat,
            x=step_names,
            y=[s[key] for s in steps],
            marker_color=color,
        ))

    fig.update_layout(
        barmode="stack",
        title=t("cost_buildup"),
        xaxis_title=t("col_step"),
        yaxis_title=f"{t('cogs_per_unit')} ({st.session_state.get('currency', 'EUR')})",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
    )
    return fig


def build_pie_chart(results: dict) -> go.Figure:
    """Build pie chart showing global cost breakdown."""
    steps = results["steps"]
    total_material = sum(s["material"] for s in steps)
    total_dl = sum(s["dl"] for s in steps)
    total_voh = sum(s["voh"] for s in steps)
    total_foh = sum(s["foh"] for s in steps)
    total_scrap = results["scrap_cost_per_unit"]

    labels = [t("col_material"), t("col_dl"), "VOH", "FOH", t("scrap_cost")]
    values = [total_material, total_dl, total_voh, total_foh, max(total_scrap, 0)]
    colors = [COLORS["material"], COLORS["dl"], COLORS["voh"], COLORS["foh"], COLORS["scrap"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo="label+percent",
        hole=0.3,
    )])
    fig.update_layout(
        title=t("cost_breakdown"),
        height=450,
    )
    return fig


def build_tornado_chart(impacts: list, top_n: int = 15) -> go.Figure:
    """Build tornado (horizontal bar) chart for sensitivity analysis."""
    top = impacts[:top_n]
    top = list(reversed(top))  # Bottom-up for tornado

    param_names = [i["param"] for i in top]
    highs = [i["impact_high"] for i in top]
    lows = [i["impact_low"] for i in top]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="+10%",
        y=param_names,
        x=highs,
        orientation="h",
        marker_color="#e74c3c",
    ))
    fig.add_trace(go.Bar(
        name="-10%",
        y=param_names,
        x=lows,
        orientation="h",
        marker_color="#3498db",
    ))

    fig.update_layout(
        barmode="overlay",
        title=t("tornado_title"),
        xaxis_title=f"{t('impact')} ({st.session_state.get('currency', 'EUR')})",
        height=max(400, top_n * 30),
        yaxis=dict(automargin=True),
    )
    return fig


def build_scenario_chart(base_results: dict, scenario_results: list,
                         scenario_names: list) -> go.Figure:
    """Build grouped stacked bar chart comparing scenarios."""
    all_data = [(t("base"), base_results)] + list(zip(scenario_names, scenario_results))

    fig = go.Figure()
    for cat, key, color in [
        (t("col_material"), "material", COLORS["material"]),
        (t("col_dl"), "dl", COLORS["dl"]),
        ("VOH", "voh", COLORS["voh"]),
        ("FOH", "foh", COLORS["foh"]),
        (t("scrap_cost"), "scrap_cost", COLORS["scrap"]),
    ]:
        x_labels = []
        y_values = []
        for name, res in all_data:
            steps = res["steps"]
            total = sum(s[key] for s in steps)
            if key == "scrap_cost":
                total = max(res.get("scrap_cost_per_unit", 0), 0)
            x_labels.append(name)
            y_values.append(round(total, 4))

        fig.add_trace(go.Bar(
            name=cat,
            x=x_labels,
            y=y_values,
            marker_color=color,
        ))

    fig.update_layout(
        barmode="stack",
        title=t("scenario_comparison"),
        yaxis_title=f"{t('cogs_per_unit')} ({st.session_state.get('currency', 'EUR')})",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


# ─── Load CSS ────────────────────────────────────────────────────────────────────
if os.path.exists(CSS_PATH):
    css = load_custom_css(CSS_PATH)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ─── Top anchor ──────────────────────────────────────────────────────────────────
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

# ─── Session State initialization ────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "nav_gen_idx" not in st.session_state:
    st.session_state.nav_gen_idx = 0
if "nav_study_idx" not in st.session_state:
    st.session_state.nav_study_idx = None
if "nav_annex_idx" not in st.session_state:
    st.session_state.nav_annex_idx = None
if "steps_data" not in st.session_state:
    st.session_state.steps_data = None
if "volume" not in st.session_state:
    st.session_state.volume = 100000
if "currency" not in st.session_state:
    st.session_state.currency = "EUR"
if "nb_steps" not in st.session_state:
    st.session_state.nb_steps = 3


# ─── Navigation ─────────────────────────────────────────────────────────────────
def set_nav(section: str, idx: int):
    """Update navigation with mutual exclusion."""
    if section == "gen":
        st.session_state.nav_gen_idx = idx
        st.session_state.nav_study_idx = None
        st.session_state.nav_annex_idx = None
    elif section == "study":
        st.session_state.nav_gen_idx = None
        st.session_state.nav_study_idx = idx
        st.session_state.nav_annex_idx = None
    elif section == "annex":
        st.session_state.nav_gen_idx = None
        st.session_state.nav_study_idx = None
        st.session_state.nav_annex_idx = idx


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title(t("sidebar_title"))
    authenticator.logout()
    st.divider()

    # Language toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            t("lang_fr"),
            type="primary" if st.session_state.lang == "fr" else "secondary",
            use_container_width=True,
        ):
            st.session_state.lang = "fr"
            st.rerun()
    with col2:
        if st.button(
            t("lang_en"),
            type="primary" if st.session_state.lang == "en" else "secondary",
            use_container_width=True,
        ):
            st.session_state.lang = "en"
            st.rerun()

    st.divider()
    st.subheader(t("nav_header"))

    # General section
    st.caption(f"**{t('gen_header')}**")
    for i, page in enumerate(t("gen_pages")):
        is_active = st.session_state.nav_gen_idx == i
        if st.button(
            page,
            key=f"nav_gen_{i}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            set_nav("gen", i)
            st.rerun()

    # Studies section
    st.caption(f"**{t('study_header')}**")
    for i, page in enumerate(t("study_pages")):
        is_active = st.session_state.nav_study_idx == i
        if st.button(
            page,
            key=f"nav_study_{i}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            set_nav("study", i)
            st.rerun()

    # Annexes section
    st.caption(f"**{t('annex_header')}**")
    for i, page in enumerate(t("annex_pages")):
        is_active = st.session_state.nav_annex_idx == i
        if st.button(
            page,
            key=f"nav_annex_{i}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            set_nav("annex", i)
            st.rerun()

    st.divider()

    # Load sample data
    if st.button(t("load_sample"), help=t("load_sample_help"), use_container_width=True):
        sample = load_sample_data()
        sample_to_session(sample)
        st.toast(t("data_loaded"))
        st.rerun()

    # Export
    if st.session_state.steps_data is not None:
        st.download_button(
            label=t("export_json"),
            data=session_to_json(),
            file_name="cogs_export.json",
            mime="application/json",
            use_container_width=True,
        )

    st.divider()
    lang = st.session_state.get("lang", "fr")
    notes = VERSION_NOTES.get(lang, VERSION_NOTES["fr"])
    st.markdown(
        t("version_info").format(version=VERSION, date=VERSION_DATE, notes=notes),
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════════
#  PAGE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════════

# ─── PAGE: Home ──────────────────────────────────────────────────────────────────
def page_home():
    lang = st.session_state.get("lang", "fr")
    path = os.path.join(DOC_PATH, lang, "accueil.md")
    if os.path.exists(path):
        content = load_file_content(path)
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error(t("no_data"))


# ─── PAGE: COGS Simulator ───────────────────────────────────────────────────────
def page_simulator():
    st.title(t("gen_pages")[1])

    if st.session_state.steps_data is None:
        st.info(t("no_data"))
        return

    # Global parameters (top bar)
    st.subheader(t("global_params"))
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        volume = st.number_input(
            t("volume"), min_value=1, value=st.session_state.volume,
            step=1000, key="inp_volume",
        )
        st.session_state.volume = volume
    with gc2:
        currency = st.text_input(t("currency"), value=st.session_state.currency, key="inp_currency")
        st.session_state.currency = currency
    with gc3:
        nb_steps = st.number_input(
            t("nb_steps"), min_value=1, max_value=20,
            value=st.session_state.nb_steps, key="inp_nb_steps",
        )
        # Adjust steps_data length if needed
        while len(st.session_state.steps_data) < nb_steps:
            st.session_state.steps_data.append({
                "name": {"fr": f"Étape {len(st.session_state.steps_data) + 1}",
                         "en": f"Step {len(st.session_state.steps_data) + 1}"},
                "uph": 60, "availability": 0.90, "performance": 0.85, "yield": 0.95,
                "nb_operators": 1, "dl_rate": 25.0, "voh_rate": 30.0, "foh_total": 50000,
                "bom": [],
            })
        while len(st.session_state.steps_data) > nb_steps:
            st.session_state.steps_data.pop()
        st.session_state.nb_steps = nb_steps

    st.divider()

    # Per-step expanders
    for step_idx in range(nb_steps):
        step = st.session_state.steps_data[step_idx]
        step_label = f"{t('step')} {step_idx + 1} : {get_step_name(step)}"

        with st.expander(step_label, expanded=(step_idx == 0)):
            # Step name
            lang = st.session_state.get("lang", "fr")
            current_name = get_step_name(step)
            new_name = st.text_input(
                t("step_name"), value=current_name,
                key=f"step_name_{step_idx}",
            )
            if isinstance(step["name"], dict):
                step["name"][lang] = new_name
            else:
                step["name"] = {lang: new_name}

            # ── Process section ──
            st.markdown(f"**{t('process_title')}**")
            pc1, pc2, pc3, pc4 = st.columns(4)
            with pc1:
                step["uph"] = st.number_input(
                    t("uph"), min_value=1, value=int(step.get("uph", 60)),
                    key=f"uph_{step_idx}",
                )
            with pc2:
                step["availability"] = st.slider(
                    t("availability"), 0.0, 1.0,
                    value=float(step.get("availability", 0.90)),
                    step=0.01, format="%.2f",
                    key=f"avail_{step_idx}",
                )
            with pc3:
                step["performance"] = st.slider(
                    t("performance"), 0.0, 1.0,
                    value=float(step.get("performance", 0.85)),
                    step=0.01, format="%.2f",
                    key=f"perf_{step_idx}",
                )
            with pc4:
                step["yield"] = st.slider(
                    t("yield"), 0.0, 1.0,
                    value=float(step.get("yield", 0.95)),
                    step=0.01, format="%.2f",
                    key=f"yield_{step_idx}",
                )

            # Info metrics
            eff_uph = step["uph"] * step["availability"] * step["performance"]
            oee = step["availability"] * step["performance"] * step["yield"]
            ic1, ic2 = st.columns(2)
            with ic1:
                st.metric(t("effective_uph"), f"{eff_uph:.1f}")
            with ic2:
                st.metric(t("oee"), f"{oee * 100:.1f}%")

            # ── Costs section ──
            st.markdown(f"**{t('costs_title')}**")
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1:
                step["nb_operators"] = st.number_input(
                    t("nb_operators"), min_value=1, value=int(step.get("nb_operators", 1)),
                    key=f"ops_{step_idx}",
                )
            with cc2:
                step["dl_rate"] = st.number_input(
                    t("dl_rate"), min_value=0.0,
                    value=float(step.get("dl_rate", 25.0)),
                    step=0.5, format="%.2f",
                    key=f"dl_{step_idx}",
                )
            with cc3:
                step["voh_rate"] = st.number_input(
                    t("voh_rate"), min_value=0.0,
                    value=float(step.get("voh_rate", 30.0)),
                    step=0.5, format="%.2f",
                    key=f"voh_{step_idx}",
                )
            with cc4:
                step["foh_total"] = st.number_input(
                    t("foh_total"), min_value=0.0,
                    value=float(step.get("foh_total", 50000)),
                    step=1000.0, format="%.0f",
                    key=f"foh_{step_idx}",
                )

            # ── BOM section ──
            st.markdown(f"**{t('bom_title')}**")
            bom = step.get("bom", [])

            for comp_idx in range(len(bom)):
                comp = bom[comp_idx]
                bc1, bc2, bc3, bc4, bc5 = st.columns([3, 1, 1, 1, 1])
                with bc1:
                    comp_name = get_component_name(comp)
                    new_comp_name = st.text_input(
                        t("component"), value=comp_name,
                        key=f"comp_name_{step_idx}_{comp_idx}",
                    )
                    if isinstance(comp.get("name"), dict):
                        comp["name"][lang] = new_comp_name
                    else:
                        comp["name"] = {lang: new_comp_name}
                with bc2:
                    comp["qty"] = st.number_input(
                        t("qty"), min_value=0.0,
                        value=float(comp.get("qty", 1)),
                        step=1.0, format="%.2f",
                        key=f"comp_qty_{step_idx}_{comp_idx}",
                    )
                with bc3:
                    comp["price"] = st.number_input(
                        t("price"), min_value=0.0,
                        value=float(comp.get("price", 0)),
                        step=0.01, format="%.4f",
                        key=f"comp_price_{step_idx}_{comp_idx}",
                    )
                with bc4:
                    comp["scrap"] = st.number_input(
                        t("scrap_rate"), min_value=0.0, max_value=0.99,
                        value=float(comp.get("scrap", 0)),
                        step=0.01, format="%.2f",
                        key=f"comp_scrap_{step_idx}_{comp_idx}",
                    )
                with bc5:
                    if st.button(t("remove"), key=f"rm_comp_{step_idx}_{comp_idx}"):
                        bom.pop(comp_idx)
                        st.rerun()

            if st.button(t("add_component"), key=f"add_comp_{step_idx}"):
                bom.append({
                    "name": {"fr": "Nouveau composant", "en": "New component"},
                    "qty": 1, "price": 0.0, "scrap": 0.0,
                })
                st.rerun()

            step["bom"] = bom

    st.divider()

    # ── RESULTS (live, no button) ──
    st.subheader(t("results_title"))
    results = compute_cogs(st.session_state.steps_data, st.session_state.volume)

    # Key metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(t("cogs_per_unit"), f"{results['cogs_per_unit']:.2f} {currency}")
    with m2:
        st.metric(t("rty"), f"{results['rty'] * 100:.1f}%")
    with m3:
        st.metric(t("units_to_start"), f"{results['units_to_start']:,.0f}")
    with m4:
        st.metric(t("scrap_cost"), f"{results['scrap_cost_per_unit']:.2f} {currency}")

    # Charts
    chart1, chart2 = st.columns(2)
    with chart1:
        fig_waterfall = build_waterfall_chart(results)
        st.plotly_chart(fig_waterfall, use_container_width=True)
    with chart2:
        fig_pie = build_pie_chart(results)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Detail table
    st.subheader(t("detail_table"))
    df = pd.DataFrame(results["steps"])
    display_cols = {
        "name": t("col_step"),
        "material": t("col_material"),
        "dl": t("col_dl"),
        "voh": t("col_voh"),
        "foh": t("col_foh"),
        "cost_added": t("col_cost_added"),
        "yield": t("col_yield"),
        "yielded_cost": t("col_yielded_cost"),
        "scrap_cost": t("col_scrap_cost"),
    }
    df_display = df[list(display_cols.keys())].rename(columns=display_cols)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Total COGS
    st.metric(t("total_cogs"), f"{results['total_cogs']:,.2f} {currency}")

    st.divider()

    # ── Price / Margin calculator ──
    st.subheader(t("price_margin_title"))
    cogs_unit = results["cogs_per_unit"]

    pm1, pm2 = st.columns(2)
    with pm1:
        mode = st.radio(
            t("calc_mode"),
            [t("margin_to_price"), t("price_to_margin")],
            key="price_margin_mode",
            horizontal=True,
        )
    with pm2:
        if mode == t("margin_to_price"):
            margin_pct = st.slider(
                t("target_margin"), 0.0, 80.0, 30.0,
                step=0.5, key="target_margin_slider",
            )
            if margin_pct < 100:
                selling_price = cogs_unit / (1 - margin_pct / 100)
                profit = selling_price - cogs_unit
                rp1, rp2, rp3 = st.columns(3)
                with rp1:
                    st.metric(t("price_result"), f"{selling_price:.2f} {currency}")
                with rp2:
                    st.metric(t("unit_profit"), f"{profit:.2f} {currency}")
                with rp3:
                    st.metric(t("cogs_per_unit"), f"{cogs_unit:.2f} {currency}")
        else:
            selling_price = st.number_input(
                t("selling_price"), min_value=0.01,
                value=max(cogs_unit * 1.5, 0.01),
                step=0.1, format="%.2f",
                key="selling_price_input",
            )
            margin_pct = (selling_price - cogs_unit) / selling_price * 100 if selling_price > 0 else 0
            profit = selling_price - cogs_unit
            rp1, rp2, rp3 = st.columns(3)
            with rp1:
                st.metric(t("margin_result"), f"{margin_pct:.1f}%")
            with rp2:
                st.metric(t("unit_profit"), f"{profit:.2f} {currency}")
            with rp3:
                st.metric(t("cogs_per_unit"), f"{cogs_unit:.2f} {currency}")


# ─── PAGE: Sensitivity Analysis ─────────────────────────────────────────────────
def page_sensitivity():
    st.title(t("sensitivity_title"))
    st.markdown(t("sensitivity_desc"))

    if st.session_state.steps_data is None:
        st.info(t("no_data"))
        return

    impacts = run_sensitivity(st.session_state.steps_data, st.session_state.volume)

    if not impacts:
        st.warning(t("no_data"))
        return

    fig = build_tornado_chart(impacts, top_n=15)
    st.plotly_chart(fig, use_container_width=True)

    # Detail table
    st.subheader(t("detail_table"))
    df = pd.DataFrame(impacts[:15])
    df_display = df[["param", "impact_high", "impact_low", "impact"]].rename(columns={
        "param": t("param_name"),
        "impact_high": "+10%",
        "impact_low": "-10%",
        "impact": t("impact"),
    })
    st.dataframe(df_display, use_container_width=True, hide_index=True)


# ─── PAGE: What-if Scenarios ────────────────────────────────────────────────────
def page_scenarios():
    st.title(t("scenarios_title"))
    st.markdown(t("scenarios_desc"))

    if st.session_state.steps_data is None:
        st.info(t("no_data"))
        return

    base_results = compute_cogs(st.session_state.steps_data, st.session_state.volume)
    currency = st.session_state.get("currency", "EUR")

    nb_scenarios = st.number_input(
        t("nb_scenarios"), min_value=1, max_value=3, value=1, key="nb_scenarios_input",
    )

    # Parameter options for modification
    param_options_keys = [
        "volume", "uph", "availability", "performance", "yield",
        "nb_operators", "dl_rate", "voh_rate", "foh_total",
    ]
    param_options_labels = [t(k) for k in param_options_keys]

    step_names = [get_step_name(s) for s in st.session_state.steps_data]

    scenario_results = []
    scenario_names = []

    for sc_idx in range(nb_scenarios):
        st.divider()
        sc_label = f"{t('scenario')} {sc_idx + 1}"
        st.subheader(sc_label)

        sc_name = st.text_input(
            t("scenario_name"), value=f"{t('scenario')} {sc_idx + 1}",
            key=f"sc_name_{sc_idx}",
        )
        scenario_names.append(sc_name)

        # Initialize modifications list in session state
        mod_key = f"sc_mods_{sc_idx}"
        if mod_key not in st.session_state:
            st.session_state[mod_key] = []

        # Display existing modifications
        mods = st.session_state[mod_key]
        for mod_idx, mod in enumerate(mods):
            mc1, mc2, mc3, mc4 = st.columns([2, 2, 2, 1])
            with mc1:
                param_sel = st.selectbox(
                    t("scenario_param"),
                    param_options_labels,
                    index=param_options_labels.index(mod.get("param_label", param_options_labels[0])),
                    key=f"sc_param_{sc_idx}_{mod_idx}",
                )
                mod["param_label"] = param_sel
                mod["param_key"] = param_options_keys[param_options_labels.index(param_sel)]
            with mc2:
                if mod["param_key"] == "volume":
                    step_sel = t("all_steps")
                    mod["step_idx"] = -1
                else:
                    step_sel = st.selectbox(
                        t("scenario_step_select"),
                        step_names,
                        index=min(mod.get("step_idx", 0), len(step_names) - 1),
                        key=f"sc_step_{sc_idx}_{mod_idx}",
                    )
                    mod["step_idx"] = step_names.index(step_sel)
            with mc3:
                mod["new_value"] = st.number_input(
                    t("scenario_new_value"),
                    value=float(mod.get("new_value", 0)),
                    format="%.4f",
                    key=f"sc_val_{sc_idx}_{mod_idx}",
                )
            with mc4:
                if st.button(t("remove"), key=f"sc_rm_{sc_idx}_{mod_idx}"):
                    mods.pop(mod_idx)
                    st.rerun()

        if st.button(t("add_modification"), key=f"sc_add_{sc_idx}"):
            mods.append({
                "param_key": "uph",
                "param_label": t("uph"),
                "step_idx": 0,
                "new_value": 0.0,
            })
            st.rerun()

        # Compute scenario
        sc_steps = deepcopy(st.session_state.steps_data)
        sc_volume = st.session_state.volume

        for mod in mods:
            pkey = mod["param_key"]
            sidx = mod["step_idx"]
            nval = mod["new_value"]

            if pkey == "volume":
                sc_volume = max(1, int(nval))
            elif sidx >= 0 and sidx < len(sc_steps):
                sc_steps[sidx][pkey] = nval

        sc_result = compute_cogs(sc_steps, sc_volume)
        scenario_results.append(sc_result)

        # Scenario metrics
        sm1, sm2, sm3 = st.columns(3)
        with sm1:
            st.metric(
                t("cogs_per_unit"),
                f"{sc_result['cogs_per_unit']:.2f} {currency}",
                delta=f"{sc_result['cogs_per_unit'] - base_results['cogs_per_unit']:.2f}",
            )
        with sm2:
            st.metric(
                t("rty"),
                f"{sc_result['rty'] * 100:.1f}%",
                delta=f"{(sc_result['rty'] - base_results['rty']) * 100:.1f}%",
            )
        with sm3:
            st.metric(
                t("total_cogs"),
                f"{sc_result['total_cogs']:,.2f} {currency}",
                delta=f"{sc_result['total_cogs'] - base_results['total_cogs']:,.2f}",
            )

    # Comparison chart
    if scenario_results:
        st.divider()
        st.subheader(t("scenario_comparison"))
        fig = build_scenario_chart(base_results, scenario_results, scenario_names)
        st.plotly_chart(fig, use_container_width=True)

        # Summary table
        rows = [{
            t("scenario"): t("base"),
            t("cogs_per_unit"): f"{base_results['cogs_per_unit']:.2f}",
            t("rty"): f"{base_results['rty'] * 100:.1f}%",
            t("total_cogs"): f"{base_results['total_cogs']:,.2f}",
            t("scenario_delta"): "-",
        }]
        for name, res in zip(scenario_names, scenario_results):
            delta = res["cogs_per_unit"] - base_results["cogs_per_unit"]
            rows.append({
                t("scenario"): name,
                t("cogs_per_unit"): f"{res['cogs_per_unit']:.2f}",
                t("rty"): f"{res['rty'] * 100:.1f}%",
                t("total_cogs"): f"{res['total_cogs']:,.2f}",
                t("scenario_delta"): f"{delta:+.2f} ({delta / base_results['cogs_per_unit'] * 100:+.1f}%)" if base_results["cogs_per_unit"] > 0 else "-",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─── PAGE: Methodology ──────────────────────────────────────────────────────────
def page_methodology():
    lang = st.session_state.get("lang", "fr")
    path = os.path.join(DOC_PATH, lang, "methodology.md")
    if os.path.exists(path):
        content = load_file_content(path)
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error(t("no_data"))


# ═════════════════════════════════════════════════════════════════════════════════
#  ROUTING
# ═════════════════════════════════════════════════════════════════════════════════
if st.session_state.nav_gen_idx == 0:
    page_home()
elif st.session_state.nav_gen_idx == 1:
    page_simulator()
elif st.session_state.nav_study_idx == 0:
    page_sensitivity()
elif st.session_state.nav_study_idx == 1:
    page_scenarios()
elif st.session_state.nav_annex_idx == 0:
    page_methodology()
else:
    page_home()

# ─── Bottom anchor ───────────────────────────────────────────────────────────────
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)

# ─── Scroll nav (up/down) ───────────────────────────────────────────────────────
st.markdown(
    '<div class="scroll-nav">'
    '<a href="#top" title="Haut">&#9650;</a>'
    '<a href="#bottom" title="Bas">&#9660;</a>'
    '</div>',
    unsafe_allow_html=True,
)
