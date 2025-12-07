import streamlit as st
from dataset_page import dataset_page
from graphs_page import graphs_page

# --- Navigation simple avec session_state ---
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

def go_to(page_name):
    st.session_state.page = page_name

# --- Sidebar navigation ---
st.sidebar.title("Navigation")
st.sidebar.button("Accueil", on_click=lambda: go_to("Accueil"))
st.sidebar.button("Jeu de données", on_click=lambda: go_to("Dataset"))
st.sidebar.button("Graphiques", on_click=lambda: go_to("Graphiques"))
st.sidebar.button("WordCloud", on_click=lambda: go_to("WordCloud"))

# --- Pages ---
def accueil():
    st.title("📊 Projet : Global Health Statistics")
    st.subheader("📄 Présentation du dataset")
    st.write("""
Le dataset utilisé s'appelle **Global Health Statistics**.  
Il provient de la plateforme **Kaggle** et rassemble des indicateurs de santé publique.
    """)
    st.subheader("🎯 Objectif du projet")
    st.write("""
- Comprendre la structure du dataset  
- Identifier les valeurs manquantes  
- Nettoyer les données  
- Analyser et visualiser des tendances mondiales
    """)
    st.markdown("""
    <hr>
    <p style='text-align:center; color:grey;'>
    DU Data Analytics – Université Paris 1 Panthéon-Sorbonne
    </p>
    """, unsafe_allow_html=True)

def graphiques_page():
    st.title("📈 Graphiques")
    st.write("Cette page affichera des visualisations (à coder ensuite).")

def wordcloud_page():
    st.title("☁️ WordCloud")
    st.write("Cette page affichera un nuage de mots (à coder ensuite).")

# --- Router ultra simple ---
if st.session_state.page == "Accueil":
    accueil()
elif st.session_state.page == "Dataset":
    dataset_page()  # <-- appelle la fonction importée depuis dataset_page.py
elif st.session_state.page == "Graphiques":
    graphs_page()
elif st.session_state.page == "WordCloud":
    wordcloud_page()
