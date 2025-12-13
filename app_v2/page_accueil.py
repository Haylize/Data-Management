import streamlit as st
import pandas as pd

from page_dataset import dataset_page
from page_dataset import wordcloud_page
from page_graph import graphs_page


st.set_page_config(
    page_title="Global Health Dashboard",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Global Health Dashboard")

st.markdown("""
Application Streamlit développée dans le cadre du module  
**Data Management, Data Visualisation & Text Mining**.

Le dataset utilisé étant volumineux et probablement **synthétique**,
l’analyse se concentre sur :
- des **agrégations**
- des **distributions**
- des **classements**
""")

DATA_PATH = "../ProjetDM/app_v2/healthstatistics.csv"


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Fichier introuvable : {DATA_PATH}")
    st.stop()


st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Aller à :",
    ["📊 Dataset", "📈 Visualisations", "☁️ WordCloud"],
)

if page == "📊 Dataset":
    dataset_page(df)
elif page == "📈 Visualisations":
    graphs_page(df)
else:
    wordcloud_page()
