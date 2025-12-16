import streamlit as st
import pandas as pd
import plotly.express as px

# Fonction principale de la page Visualisations
def graphs_page(df: pd.DataFrame) -> None:
    # Titre de la page
    st.header("📈 Visualisations & Analyses")
    # Texte de présentation de la page
    st.markdown("""
    Cette page propose plusieurs visualisations interactives permettant
    d’explorer les données sous différents angles :
    géographique, médical, économique et temporel.
    """)

    # --- Filtres ---
    st.sidebar.subheader("🎛️ Filtres")
    # Sélection de l’année via un slider
    year = st.sidebar.slider(
        "Année",
        int(df["Year"].min()),
        int(df["Year"].max()),
        int(df["Year"].max()),
    )

    # Sélection d’un pays ou de plusieurs pays
    country = st.sidebar.selectbox(
        "Pays",
        ["Tous"] + sorted(df["Country"].unique())
    )
    
    # Filtrage des données selon l’année sélectionnée
    fdf = df[df["Year"] == year]
    if country != "Tous":
        fdf = fdf[fdf["Country"] == country]
        
    # Dataset filtré uniquement par année
    filtered_df = df[df["Year"] == year]


    # 1. Carte mondiale (agrégée)

    st.subheader("🌍 Indicateurs de santé par pays")
    # Agrégation des indicateurs par pays
    map_df = (
        fdf.groupby("Country", observed=True)
        .agg(
            avg_mortality=("Mortality Rate (%)", "mean"),
            avg_recovery=("Recovery Rate (%)", "mean"),
            population=("Population Affected", "sum"),
        )
        .reset_index()         # transforme l’index en colonne classique

    )
    
    # Création de la carte mondiale
    fig_map = px.scatter_geo(
        map_df,
        locations="Country",
        locationmode="country names",
        size="avg_mortality",  # taille des points proportionnelle à la mortalité
        color="avg_recovery",  # couleur basée sur le taux de rétablissement
        hover_name="Country",
        title=f"Indicateurs agrégés — {year}",
    )
    # Affichage de la carte
    st.plotly_chart(fig_map, use_container_width=True)

    st.caption("Taille = mortalité moyenne | Couleur = rétablissement moyen")

 
    # 2. Top maladies

    st.subheader("🦠 Top 10 maladies les plus mortelles")
    
    # Calcul de la mortalité moyenne par maladie
    top_disease = (
        fdf.groupby("Disease Name", observed=True)["Mortality Rate (%)"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    
    # Graphique en barres
    fig_disease = px.bar(
        top_disease,
        x="Disease Name",
        y="Mortality Rate (%)",
    )
    st.plotly_chart(fig_disease, use_container_width=True)


    # 3. Coût total par catégorie

    st.subheader("Coût total estimé par type de maladie")
    
    # Copie du DataFrame pour créer une variable dérivée
    fdf = fdf.copy()
    # Calcul du coût total (coût moyen * population affectée)
    fdf["Total Cost"] = (
        fdf["Average Treatment Cost (USD)"] * fdf["Population Affected"]
    )
    
    # Agrégation des coûts par catégorie de maladie
    cost_cat = (
        fdf.groupby("Disease Category", observed=True)["Total Cost"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    
    # Graphique en barres des coûts
    fig_cost = px.bar(
        cost_cat,
        x="Disease Category",
        y="Total Cost",
    )
    st.plotly_chart(fig_cost, use_container_width=True)


    # 4. ACCÈS AUX SOINS VS MORTALITÉ

    st.subheader("🏥 Accès aux soins vs mortalité")
    
    # Nuage de points entre accès aux soins et mortalité
    fig_access = px.scatter(
        filtered_df,
        x="Healthcare Access (%)",
        y="Mortality Rate (%)",
        opacity=0.4              # transparence pour mieux voir les zones denses
        title="Relation entre accès aux soins et mortalité"
    )

    st.plotly_chart(fig_access, use_container_width=True)

    st.caption("Tendance attendue : plus l’accès aux soins est élevé, plus la mortalité diminue.")


    # 5. REVENU VS TAUX DE RÉTABLISSEMENT

    st.subheader("Revenu par habitant vs taux de rétablissement")

    # Nuage de points entre revenu et taux de rétablissement
    fig_income = px.scatter(
        filtered_df,
        x="Per Capita Income (USD)",
        y="Recovery Rate (%)",
        opacity=0.4,
        title="Impact du revenu sur le taux de rétablissement"
    )

    st.plotly_chart(fig_income, use_container_width=True)


    # 6. Distributions

    st.subheader("Distributions (échantillon)")
    # Échantillon pour alléger le calcul et l’affichage
    sample = fdf.sample(min(50_000, len(fdf)), random_state=42)
    
    # Boxplot de la mortalité par catégorie de maladie
    fig_box = px.box(
        sample,
        x="Disease Category",
        y="Mortality Rate (%)",
        title="Distribution de la mortalité par catégorie",
    )
    st.plotly_chart(fig_box, use_container_width=True)


    # 7. Évolution temporelle

    st.subheader("Évolution globale de la mortalité")
    
    # Calcul de la mortalité moyenne par année
    time_df = (
        df.groupby("Year", observed=True)["Mortality Rate (%)"]
        .mean()
        .reset_index()
    )

    # Graphique de l’évolution temporelle
    fig_time = px.line(
        time_df,
        x="Year",
        y="Mortality Rate (%)",
    )
    st.plotly_chart(fig_time, use_container_width=True)



    st.info("""
    Les visualisations confirment une forte homogénéité des données.
    L’intérêt de l’analyse repose donc sur la **structuration**, la
    **comparaison** et l’**exploration interactive** du dataset.
    """)
