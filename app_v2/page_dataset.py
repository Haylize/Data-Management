import streamlit as st
import pandas as pd


@st.cache_data(show_spinner=False)
def descriptive_stats(df: pd.DataFrame, sample_size: int = 200_000) -> pd.DataFrame:
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=42)

    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")

    return df.describe(include="number").T


def dataset_page(df: pd.DataFrame) -> None:
    st.header("📊 Présentation du jeu de données")

    st.markdown("""
    Cette page présente une **analyse exploratoire (EDA)** du dataset :
    structure, types de variables, valeurs manquantes et statistiques descriptives.
    """)

    # --- Dimensions ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", f"{df.shape[0]:,}".replace(",", " "))
    col2.metric("Colonnes", df.shape[1])
    col3.metric("Mémoire (MB)", f"{df.memory_usage(deep=True).sum() / 1e6:.1f}")

    # --- Aperçu ---
    st.subheader("👀 Aperçu des données")
    st.dataframe(df.head(20), use_container_width=True)

    # --- Types ---
    st.subheader("🧬 Types de variables")
    st.dataframe(
        pd.DataFrame({"Type": df.dtypes.astype(str)}),
        use_container_width=True,
    )

    # --- Valeurs manquantes ---
    st.subheader("❗ Valeurs manquantes")
    missing_df = pd.DataFrame({
        "Missing count": df.isna().sum(),
        "Missing (%)": (df.isna().mean() * 100).round(2),
    }).sort_values("Missing (%)", ascending=False)

    st.dataframe(missing_df, use_container_width=True)

    # --- Stats descriptives ---
    st.subheader("📈 Statistiques descriptives (numériques)")

    sample_size = st.slider(
        "Taille d’échantillon pour les statistiques",
        min_value=50_000,
        max_value=min(500_000, len(df)),
        value=min(200_000, len(df)),
        step=50_000,
    )

    stats = descriptive_stats(df, sample_size)
    st.dataframe(stats, use_container_width=True)

    st.info("""
    Les statistiques montrent des valeurs très homogènes.
    Cela suggère un **dataset synthétique**, ce qui justifie l’utilisation
    d’analyses agrégées et de distributions dans la suite.
    """)

    # ===============================
    # Valeurs manquantes
    # ===============================
    st.subheader("❗ Valeurs manquantes")
    missing_df = pd.DataFrame({
        "Nombre": df.isna().sum(),
        "Pourcentage (%)": (df.isna().mean() * 100).round(2)
    }).sort_values("Pourcentage (%)", ascending=False)

    st.dataframe(missing_df, use_container_width=True)


    # ===============================
    # Variable dérivée (sécurisée)
    # ===============================
    st.subheader("➕ Variable dérivée")

    if (
        "Average Treatment Cost (USD)" in df.columns
        and "Population Affected" in df.columns
    ):
        df["Economic_Burden"] = (
            df["Average Treatment Cost (USD)"] * df["Population Affected"]
        )
        st.success("Variable **Economic_Burden** (Average Treatment Cost (USD) * Population Affected) créée avec succès.")
    else:
        st.warning("Colonnes nécessaires absentes pour créer Economic_Burden.")


def wordcloud_page():
    st.title("☁️ WordCloud")
    st.write("Cette page affichera un nuage de mots (à coder ensuite).")