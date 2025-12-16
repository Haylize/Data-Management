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

Le dataset contient des informations sur :

- Les pays
- Les maladies et catégories de maladies
- Les taux de prévalence, incidence et mortalité
- La population affectée
- L’accès aux soins (Healthcare Access, Doctors per 1000, Hospital Beds per 1000)
- Des variables socio-économiques (Per Capita Income, Education Index, Urbanization Rate, etc.)

---

## 📁 Structure du projet

```plaintext
app_v2/
│
├── page_accueil.py
├── page_dataset.py
├── page_graph.py
├── page_wordcloud.py
└── data/
    └── (le fichier CSV doit être ajouté ici en local)


---

## ⚙️ Installation & environnement

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/Haylize/Data-Management.git
cd Data-Management/app_v2

### Dataset (obligatoire)

⚠️ Le jeu de données n’est pas inclus dans le dépôt (taille trop importante).
Télécharger le dataset depuis Kaggle :
https://www.kaggle.com/datasets/malaiarasugraj/global-health-statistics?resource=download
Placer le fichier suivant dans le dossier :
```bash
app_v2/data/Global Health Statistics.csv

### Lancer l'application Streamlit : 

Depuis le dossier app_v2 :
```bash
streamlit run page_accueil.py
