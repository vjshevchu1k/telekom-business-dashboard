import streamlit as st
import pandas as pd
import plotly.express as px

# Titel
st.set_page_config(page_title="Telekom Business Dashboard", layout="wide")

st.title("📊 Telekom Business Dashboard")
st.markdown("Ein interaktives Dashboard zur Analyse von Umsatz, Kosten und Kundenstatistik.")

# Daten laden
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Filter
regionen = df["Region"].unique()
monate = df["Monat"].unique()

col1, col2 = st.columns(2)
with col1:
    region_filter = st.multiselect("Region auswählen:", regionen, default=regionen)
with col2:
    monat_filter = st.multiselect("Monat auswählen:", monate, default=monate)

df_filtered = df[df["Region"].isin(region_filter) & df["Monat"].isin(monat_filter)]

# KPI-Berechnung
gesamt_umsatz = df_filtered["Umsatz"].sum()
gesamt_kosten = df_filtered["Kosten"].sum()
kunden_summe = df_filtered["Kunden"].sum()
gewinn = gesamt_umsatz - gesamt_kosten

col3, col4, col5, col6 = st.columns(4)
col3.metric("💰 Gesamtumsatz", f"{gesamt_umsatz:,.0f} €")
col4.metric("💸 Gesamtkosten", f"{gesamt_kosten:,.0f} €")
col5.metric("👥 Kunden gesamt", f"{kunden_summe:,}")
col6.metric("📈 Gewinn", f"{gewinn:,.0f} €")

# Diagramme
fig_umsatz = px.bar(df_filtered, x="Monat", y="Umsatz", color="Region", barmode="group", title="Umsatz nach Monat und Region")
fig_kunden = px.line(df_filtered, x="Monat", y="Kunden", color="Region", markers=True, title="Kundenentwicklung")

st.plotly_chart(fig_umsatz, use_container_width=True)
st.plotly_chart(fig_kunden, use_container_width=True)

st.markdown("---")
st.markdown("© 2025 Telekom Business Dashboard – Erstellt von [Dein Name]")
