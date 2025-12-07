import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration (Noms des colonnes du CSV) ---
DATA_PATH = "Global_Health_Statistics.csv"
COL_COUNTRY = 'Country'
COL_DISEASE = 'Disease Name'
COL_YEAR = 'Year'
COL_MORTALITY = 'Mortality Rate (%)'
COL_RECOVERY = 'Recovery Rate (%)'
COL_COST = 'Average Treatment Cost (USD)'
COL_AGE = 'Age Group'
COL_HEALTH_ACCESS = 'Healthcare Access (%)' # Nouvelle colonne pour le graphique additionnel


# --- 1. Chargement des données ---
@st.cache_data
def load_data():
    """Charge les données du CSV sans modification (pour la simplicité)."""
    try:
        data = pd.read_csv(DATA_PATH, sep=';')
        return data
    except FileNotFoundError:
        st.error(f"Erreur: Le fichier de données '{DATA_PATH}' est introuvable. Vérifiez le nom et l'emplacement.")
        st.stop()


# --- 2. Fonction Principale de la Page ---
def graphs_page():
    st.title("📈 Analyse et Visualisations Détaillées")
    
    df = load_data()
    
    # --- A. Préparation des Listes de Filtres ---
    available_countries = sorted(df[COL_COUNTRY].dropna().unique())
    available_diseases = sorted(df[COL_DISEASE].dropna().unique())
    available_years = sorted(df[COL_YEAR].dropna().unique().astype(int))
    
    
    # --- B. Affichage des listes (Pays et Maladies) ---
    st.header("🌐 Aperçu des Dimensions")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Liste des Pays")
        st.dataframe(pd.DataFrame({'Pays': available_countries}), use_container_width=True, height=200)
    with col2:
        st.subheader("Liste des Maladies")
        st.dataframe(pd.DataFrame({'Maladies': available_diseases}), use_container_width=True, height=200)

    st.markdown("---")


    # --------------------------------------------------------------------------
    ## 💸 Graphique 1 : Coût Moyen de Traitement (Barres)
    # --------------------------------------------------------------------------
    st.header("💸 Coût Moyen de Traitement par Pays et Maladie")
    
    col_filters_cost = st.columns(2)
    with col_filters_cost[0]:
        selected_country_cost = st.selectbox(
            "Sélectionnez le Pays", options=available_countries, index=0, key='country_cost'
        )
    with col_filters_cost[1]:
        selected_disease_cost = st.selectbox(
            "Sélectionnez la Maladie", options=available_diseases, index=0, key='disease_cost'
        )
        
    df_cost_filtered = df[
        (df[COL_COUNTRY] == selected_country_cost) & 
        (df[COL_DISEASE] == selected_disease_cost)
    ].copy()
    
    if not df_cost_filtered.empty:
        # Calcule la moyenne du coût par année pour les filtres sélectionnés
        cost_by_year = df_cost_filtered.groupby(COL_YEAR)[COL_COST].mean().reset_index()
        
        fig_cost = px.bar(
            cost_by_year, 
            x=COL_YEAR, y=COL_COST, 
            title=f"Coût pour {selected_disease_cost} en {selected_country_cost}",
            labels={COL_YEAR: 'Année', COL_COST: 'Coût Moyen (USD)'}
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    else:
        st.info("Aucune donnée de coût trouvée pour cette sélection.")

    st.markdown("---")


    # --------------------------------------------------------------------------
    ## 💀 Graphique 2 : Taux de Mortalité par Groupe d'Âge (Barres)
    # --------------------------------------------------------------------------
    st.header("💀 Taux de Mortalité par Groupe d'Âge")

    col_filters_mortality = st.columns(3)
    with col_filters_mortality[0]:
        selected_country_mort = st.selectbox("Pays", options=available_countries, index=0, key='country_mort')
    with col_filters_mortality[1]:
        selected_disease_mort = st.selectbox("Maladie", options=available_diseases, index=0, key='disease_mort')
    with col_filters_mortality[2]:
        selected_year_mort = st.selectbox("Année", options=available_years, index=0, key='year_mort')

    df_mort_filtered = df[
        (df[COL_COUNTRY] == selected_country_mort) & 
        (df[COL_DISEASE] == selected_disease_mort) &
        (df[COL_YEAR] == selected_year_mort)
    ].copy()

    if not df_mort_filtered.empty:
        # Calcule la moyenne de mortalité par groupe d'âge
        mort_by_age = df_mort_filtered.groupby(COL_AGE)[COL_MORTALITY].mean().reset_index()
        
        fig_mort = px.bar(
            mort_by_age,
            x=COL_AGE, y=COL_MORTALITY,
            title=f"Mortalité par Âge pour {selected_disease_mort} ({selected_year_mort})",
            color=COL_AGE,
            labels={COL_MORTALITY: 'Taux de Mortalité (%)', COL_AGE: 'Groupe d\'Âge'}
        )
        st.plotly_chart(fig_mort, use_container_width=True)
        
    else:
        st.info("Aucune donnée de mortalité trouvée pour cette combinaison de filtres.")

    st.markdown("---")


    # --------------------------------------------------------------------------
    ## 🎯 Graphique 3 : Corrélation Accès Santé vs. Rétablissement (Dispersion)
    # --------------------------------------------------------------------------
    st.header("🎯 Analyse : Accès aux Soins vs. Taux de Rétablissement")
    st.write("Ce graphique de dispersion montre si un meilleur accès aux soins est lié à un meilleur taux de récupération, agrégé sur toutes les maladies.")

    # Agrégation sur toutes les données disponibles (pour un aperçu global)
    # On calcule la moyenne de l'accès aux soins, de la récupération et de la mortalité par pays.
    df_correlation = df.groupby(COL_COUNTRY).agg(
        avg_health_access=(COL_HEALTH_ACCESS, 'mean'),
        avg_recovery=(COL_RECOVERY, 'mean'),
        avg_mortality=(COL_MORTALITY, 'mean')
    ).reset_index().dropna()

    if not df_correlation.empty:
        fig_scatter = px.scatter(
            df_correlation,
            x='avg_health_access',
            y='avg_recovery',
            size='avg_mortality', # La taille du point représente le taux de mortalité moyen
            color='avg_mortality', # La couleur aussi, pour renforcer la visualisation
            hover_name=COL_COUNTRY,
            title="Corrélation entre l'Accès aux Soins et le Taux de Rétablissement (Toutes Années/Maladies)",
            labels={
                'avg_health_access': 'Accès aux Soins (%)',
                'avg_recovery': 'Taux de Rétablissement (%)'
            },
            color_continuous_scale=px.colors.sequential.Sunset # Pour une couleur contrastée
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("Données insuffisantes pour calculer la corrélation.")
    
    st.markdown("---")

    
    # --------------------------------------------------------------------------
    ## 🗺️ Graphique 4 : Carte Géographique (Mortalité et Rétablissement)
    # --------------------------------------------------------------------------
    st.header("🗺️ Carte Géographique : Mortalité et Rétablissement")
    st.write("La **taille** des cercles est le Taux de Mortalité ; la **couleur** est le Taux de Rétablissement. Vous pouvez changer l'année avec le curseur.")

    # Slider Année
    selected_map_year = st.slider(
        "Sélectionnez l'Année", 
        min_value=min(available_years), 
        max_value=max(available_years), 
        value=available_years[0], # Première année disponible par défaut
        step=1, 
        key='map_year_slider'
    )
    
    df_map_filtered = df[df[COL_YEAR] == selected_map_year].copy()
    
    # ⚠️ Agrégation : On fait la MOYENNE pour chaque pays et chaque année
    map_data = df_map_filtered.groupby(COL_COUNTRY).agg(
        average_mortality=(COL_MORTALITY, 'mean'),
        average_recovery=(COL_RECOVERY, 'mean')
    ).reset_index()
    
    map_data.dropna(subset=['average_mortality', 'average_recovery'], inplace=True)

    if not map_data.empty:
        fig_map = px.scatter_geo(
            map_data,
            locations=COL_COUNTRY,
            locationmode='country names', 
            hover_name=COL_COUNTRY,
            size="average_mortality", 
            color="average_recovery", 
            color_continuous_scale=px.colors.sequential.Viridis,
            projection="natural earth",
            title=f"Taux Mondiaux en {selected_map_year}",
            labels={"average_mortality": "Mortalité (%)", "average_recovery": "Rétablissement (%)"}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
    else:
        st.info(f"Aucune donnée valide trouvée pour l'année **{selected_map_year}**.")