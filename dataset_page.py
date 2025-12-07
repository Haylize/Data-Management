import streamlit as st
import pandas as pd

def dataset_page():
    st.title("📁 Présentation et Nettoyage du Jeu de Données")

    # --- Chargement du CSV ---
    try:
        df = pd.read_csv("Global_Health_Statistics.csv", sep=";")
    except FileNotFoundError:
        st.error("Fichier CSV introuvable.")
        return

    # --- Aperçu du dataset ---
    st.subheader("Aperçu des 10 premières lignes")
    st.dataframe(df.head(10))

    # --- Dimensions et types ---
    st.subheader("Dimensions et types")
    st.write(f"Lignes : {len(df):,} | Colonnes : {df.shape[1]}")
    st.dataframe(df.dtypes.to_frame("Type"))

    # --- 1. Valeurs manquantes ---
    st.subheader("Valeurs manquantes")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        st.success("✅ Aucun valeur manquante détectée dans le dataset.")
        st.info("""
**Détails :**  
- Nous avons vérifié chaque colonne du dataset pour détecter les valeurs `NaN`.  
- Colonnes numériques et catégorielles incluses.  
- Aucune donnée n’a dû être imputée car le dataset est complet.
""")
    else:
        st.warning("⚠️ Certaines valeurs manquantes détectées :")
        st.dataframe(missing.to_frame("Valeurs manquantes").sort_values("Valeurs manquantes", ascending=False))

    # --- 2. Doublons ---
    st.subheader("Doublons")
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        st.success("✅ Aucun doublon détecté.")
        st.info("""
**Détails :**  
- Nous avons comparé toutes les lignes entre elles pour identifier des doublons exacts.  
- Aucune suppression n’a été nécessaire.
""")
        # On a comparé toutes les lignes entre elles pour identifier les doublons exacts.
    else:
        st.warning(f"⚠️ {duplicates} doublons détectés et supprimés.")
        df = df.drop_duplicates()

    # --- 3. Incohérences / erreurs ---
    st.subheader("Incohérences / Erreurs")
    errors = pd.DataFrame()

    # Cette étape vérifie la cohérence des données numériques.
    # Même si le dataset semble complet, certaines valeurs pourraient être aberrantes.
    
    # Colonnes numériques représentant des taux ou pourcentages (0 à 100)
    numeric_cols = ['Prevalence Rate (%)', 'Incidence Rate (%)', 'Mortality Rate (%)',
                    'Healthcare Access (%)', 'Recovery Rate (%)', 'Improvement in 5 Years (%)',
                    'Urbanization Rate (%)']

    for col in numeric_cols:
        if col in df.columns:
            # On sélectionne les valeurs négatives ou supérieures à 100%
            invalid = df[(df[col] < 0) | (df[col] > 100)]
            if not invalid.empty:
                # On marque ces lignes comme erreurs
                invalid['Erreur'] = f"Valeur invalide dans {col}"
                errors = pd.concat([errors, invalid])

    # Colonnes économiques : revenu ou coût traitement ne doivent pas être négatifs
    if 'Per Capita Income (USD)' in df.columns:
        invalid_income = df[df['Per Capita Income (USD)'] < 0]
        if not invalid_income.empty:
            invalid_income['Erreur'] = "Revenu négatif"
            errors = pd.concat([errors, invalid_income])

    if 'Average Treatment Cost (USD)' in df.columns:
        invalid_cost = df[df['Average Treatment Cost (USD)'] < 0]
        if not invalid_cost.empty:
            invalid_cost['Erreur'] = "Coût traitement négatif"
            errors = pd.concat([errors, invalid_cost])

    # Résultat final
    if errors.empty:
        st.success("✅ Aucune incohérence ou erreur détectée dans le dataset.")
        st.info("""**Détails:**  
- Toutes les colonnes numériques ont été vérifiées pour détecter des valeurs aberrantes :  
- Taux ou pourcentages négatifs ou supérieurs à 100  
- Revenu ou coût de traitement négatif  
- Aucun problème n’a été trouvé, donc les données sont cohérentes et prêtes à l’analyse.  
""")

    else:
        st.warning(f"⚠️ {len(errors)} erreurs détectées :")
        st.dataframe(errors)
        st.info("""
**Explication :**  
Les lignes affichées contiennent des valeurs aberrantes ou impossibles qui nécessitent une correction avant analyse.  
Ce contrôle permet de garantir que les futures analyses statistiques seront fiables.
""")

# --- 4. Création de variables dérivées ---
    st.subheader("Création de nouvelles variables dérivées")

    # 1️⃣ Charge économique totale (Economic_Burden)
    df['Economic_Burden'] = df['Average Treatment Cost (USD)'] * df['Population Affected']
    st.write("**Economic_Burden** : Charge économique totale d'une maladie pour la population affectée.")
    st.info("""
- Objectif : montrer le coût total d'une maladie pour un pays ou une population.  
- Calcul : `Economic_Burden = Average Treatment Cost (USD) * Population Affected`  
- Utile pour prioriser les maladies selon leur impact économique.
""")

    # 2️⃣ Ratio médecins / population affectée (Doctors_to_Population)
    df['Doctors_to_Population'] = df['Doctors per 1000'] / df['Population Affected']
    st.write("**Doctors_to_Population** : Disponibilité des médecins par personne affectée.")
    st.info("""
- Objectif : évaluer la charge médicale par rapport au nombre de personnes touchées.  
- Calcul : `Doctors_to_Population = Doctors per 1000 / Population Affected`  
- Utile pour identifier les pays où la prise en charge médicale pourrait être insuffisante.
""")

    # --- 5. Justification et résumé ---
    st.subheader("🧹 Résumé du nettoyage et des transformations")
    st.write("""
- Dataset vérifié pour valeurs manquantes, doublons et incohérences.  
- Création de variables dérivées pour enrichir l'analyse :  
    - Economic_Burden  
    - Doctors_to_Population  
- Ces transformations ne modifient pas les données existantes mais ajoutent des informations pertinentes pour l'analyse future.
""")