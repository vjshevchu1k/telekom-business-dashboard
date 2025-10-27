import streamlit as st
import pandas as pd
import plotly.express as px

# --- Seiteneinstellungen ---
st.set_page_config(page_title="Telekom Business Dashboard", layout="wide")

# --- Titel und Beschreibung ---
st.title("📊 Telekom Business Dashboard")
st.markdown("Ein interaktives Dashboard zur Analyse von **Umsatz**, **Kosten**, **Kunden** und **Gewinn** in verschiedenen Regionen Deutschlands.")

# --- Daten laden ---
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# --- Filter ---
regionen = df["Region"].unique()
monate = df["Monat"].unique()

st.sidebar.header("🔎 Filteroptionen")
region_filter = st.sidebar.multiselect("Region auswählen:", regionen)
monat_filter = st.sidebar.multiselect("Monat auswählen:", monate)

# --- Filter anwenden ---
if not region_filter or not monat_filter:
    st.warning("⚠️ Bitte wähle mindestens **eine Region** und **einen Monat** aus, um die Daten anzuzeigen.")
    st.stop()

df_filtered = df[df["Region"].isin(region_filter) & df["Monat"].isin(monat_filter)]

# --- KPIs ---
gesamt_umsatz = df_filtered["Umsatz"].sum()
gesamt_kosten = df_filtered["Kosten"].sum()
kunden_summe = df_filtered["Kunden"].sum()
gewinn = gesamt_umsatz - gesamt_kosten

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Gesamtumsatz", f"{gesamt_umsatz:,.0f} €")
col2.metric("💸 Gesamtkosten", f"{gesamt_kosten:,.0f} €")
col3.metric("👥 Kunden gesamt", f"{kunden_summe:,}")
col4.metric("📈 Gewinn", f"{gewinn:,.0f} €")

# --- Diagramme ---
fig_umsatz = px.bar(
    df_filtered,
    x="Monat",
    y="Umsatz",
    color="Region",
    barmode="group",
    title="Umsatz nach Monat und Region"
)

fig_kunden = px.line(
    df_filtered,
    x="Monat",
    y="Kunden",
    color="Region",
    markers=True,
    title="Kundenentwicklung nach Monat"
)

st.plotly_chart(fig_umsatz, use_container_width=True)
st.plotly_chart(fig_kunden, use_container_width=True)

# --- Fußzeile ---
st.markdown("---")
st.markdown("© 2025 Telekom Business Dashboard – Erstellt von Vitalii Shevchuk")
