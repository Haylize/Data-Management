# 📘 Projet Data Management & Visualisation — SDA 2025-2026

## 🎯 Description du projet

Ce projet est réalisé dans le cadre du module **Data Management, Data Visualisation & Text Mining (SDA 2025–2026)**.

L’objectif principal est de développer une application **interactive avec Streamlit** permettant d’explorer en détail un jeu de données volumineux lié à la **santé mondiale**.

Le projet comprend :

- Analyse exploratoire des données (EDA)
- Nettoyage et préparation des données (valeurs manquantes, cohérence…)
- Création de variables dérivées
- Visualisations interactives (au moins 5 graphiques)
- Partie Text Mining (article de presse + prétraitement + WordCloud)
- Développement d’une application Streamlit complète

---

## 📊 Jeu de données

- **Nom :** Global Health Statistics  
- **Taille :** ~1 000 000 lignes (trop volumineux pour être stocké directement sur GitHub)

Le fichier CSV n’est pas inclus dans ce dépôt car il dépasse la limite de taille de GitHub.

📌 **Lien de téléchargement du dataset :**  
👉 : https://www.kaggle.com/datasets/malaiarasugraj/global-health-statistics?resource=download
Le dataset contient des informations sur :

- Les pays
- Les maladies et catégories de maladies
- Les taux de prévalence, incidence et mortalité
- La population affectée
- L’accès aux soins (Healthcare Access, Doctors per 1000, Hospital Beds per 1000)
- Des variables socio-économiques (Per Capita Income, Education Index, Urbanization Rate, etc.)

---

## 🗂️ Structure du projet

Organisation recommandée du dépôt :

    Data-Management/
    │
    ├── README.md        # Contient le lien vers le dataset 
    │
    ├── notebook/
    │   └── notebook_dm.ipynb        # Notebook Jupyter pour l’analyse exploratoire et le data management
    │
    ├── streamlit_app/
    │   └── streamlit_app.py # Application Streamlit principale
    │
    └── README.md            # Ce fichier

---

## ⚙️ Installation & environnement

1. Cloner le dépôt (ou le récupérer depuis GitHub Classroom / compte du groupe)
2. Créer un environnement virtuel Python (optionnel mais recommandé)  
3. Installer les dépendances :

    pip install -r requirements.txt

---

## ▶️ Lancer l’application Streamlit

Depuis la racine du projet :

    streamlit run app/streamlit_app.py

L’application permet notamment :

- de visualiser des statistiques descriptives
- de filtrer les données (pays, maladies, années…)
- d’afficher des graphiques interactifs
- d’explorer les résultats de la partie Text Mining

---

