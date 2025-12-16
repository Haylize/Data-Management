import streamlit as st
import pandas as pd

# Calcul des statistiques descriptives du dataset
@st.cache_data(show_spinner=False)
def descriptive_stats(df: pd.DataFrame, sample_size: int = 200_000) -> pd.DataFrame:
    # Si le nombre de lignes est trop élevé, on prend un échantillon aléatoire
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=42)

    df = df.copy()
    # Conversion des colonnes de type "object" en numérique
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")
    # Calcul des statistiques descriptives pour les variables numériques
    return df.describe(include="number").T


def dataset_page(df: pd.DataFrame) -> None:
    # Titre de la page
    st.header("📊 Présentation du jeu de données")
    # Texte explicatif de la page
    st.markdown("""
    Cette page présente une **analyse exploratoire (EDA)** du dataset :
    structure, types de variables, valeurs manquantes et statistiques descriptives.
    """)

    # --- Dimensions ---
    col1, col2, col3 = st.columns(3)
    
    # Nombre de lignes
    col1.metric("Lignes", f"{df.shape[0]:,}".replace(",", " "))
    # Nombre de colonnes
    col2.metric("Colonnes", df.shape[1])
    # Mémoire utilisée par le dataset
    col3.metric("Mémoire (MB)", f"{df.memory_usage(deep=True).sum() / 1e6:.1f}")

    # --- Aperçu ---
    st.subheader("👀 Aperçu des données")
    st.dataframe(df.head(20), use_container_width=True)

    # --- Types ---
    st.subheader("🧬 Types de variables")
    # Tableau récapitulatif des types de données par colonne
    st.dataframe(
        pd.DataFrame({"Type": df.dtypes.astype(str)}),
        use_container_width=True,
    )


    # --- Stats descriptives ---
    st.subheader("📈 Statistiques descriptives (numériques)")
    
    # Slider pour choisir la taille de l’échantillon utilisé
    sample_size = st.slider(
        "Taille d’échantillon pour les statistiques",
        min_value=50_000,
        max_value=min(500_000, len(df)),
        value=min(200_000, len(df)),
        step=50_000,
    )
    # Calcul des statistiques descriptives
    stats = descriptive_stats(df, sample_size)
    # Affichage du tableau de statistiques
    st.dataframe(stats, use_container_width=True)

    # Message d’interprétation des résultats
    st.info("""
    Les statistiques montrent des valeurs très homogènes.
    Cela suggère un **dataset synthétique**, ce qui justifie l’utilisation
    d’analyses agrégées et de distributions dans la suite.
    """)


    # --- Valeurs manquantes ---
 
    st.subheader("❗ Valeurs manquantes")
    # Calcul du nombre et du pourcentage de valeurs manquantes par variable
    missing_df = pd.DataFrame({
        "Nombre": df.isna().sum(),
        "Pourcentage (%)": (df.isna().mean() * 100).round(2)
    }).sort_values("Pourcentage (%)", ascending=False)

    # Affichage du tableau des valeurs manquantes
    st.dataframe(missing_df, use_container_width=True)
    

    # --- Variable dérivée ---

    st.subheader("➕ Variable dérivée")

    # Vérification de la présence des colonnes nécessaires
    if (
        "Average Treatment Cost (USD)" in df.columns
        and "Population Affected" in df.columns
    ):
        # Création de la variable Economic_Burden
        df["Economic_Burden"] = (
            df["Average Treatment Cost (USD)"] * df["Population Affected"]
        )
        # Message de confirmation
        st.success("Variable **Economic_Burden** (Average Treatment Cost (USD) * Population Affected) créée avec succès.")
    else:
        # Message d’alerte si les colonnes sont absentes
        st.warning("Colonnes nécessaires absentes pour créer Economic_Burden.")

