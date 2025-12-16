# page_wordcloud.py
import re
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Stopwords français de base
DEFAULT_STOPWORDS_FR = {
    "le","la","les","un","une","des","de","du","au","aux","en","et","ou","où","que","qui",
    "dans","pour","par","avec","sans","sur","ce","cet","cette","ces","se","ses","son","sa",
    "est","sont","été","être","avoir","ont","a","avait","plus","moins","comme",
    "ne","pas","encore","très","ainsi","entre","depuis","vers",
    "l","d","s","qu","à","afin","toute","tous","toutes","leur","leurs","dont","lorsque","car"
}


@st.cache_data(show_spinner=False)
def load_text(path: str) -> str:
    # Lecture du fichier texte une seule fois grâce au cache
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def preprocess_text(article: str) -> str:
    # 1) minuscules pour éviter les doublons (Santé / santé)
    text = article.lower()

    # 2) suppression ponctuation / caractères spéciaux (garde accents + apostrophe)
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿæœ\s']", " ", text)

    # 3) espaces multiples
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_filter(text: str, stopwords: set[str], min_len: int = 3) -> list[str]:
    # découpe le texte en mots à partir des espaces
    tokens = text.split()
    # ce qu'on conserve uniquement
    clean_tokens = [w for w in tokens if (w not in stopwords and len(w) >= min_len)]
    return clean_tokens


@st.cache_data(show_spinner=False)
def build_wordcloud(
    text_for_wc: str,
    width: int,
    height: int,
    background: str,
    max_words: int,
    collocations: bool,
) -> WordCloud:
    wc = WordCloud(
        width=width,
        height=height,
        background_color=background,
        max_words=max_words,
        collocations=collocations,  # évite des bigrammes parfois bizarres
    ).generate(text_for_wc)  # calcul des fréquences et création du nuage
    return wc


def wordcloud_page() -> None:
    st.header("WordCloud — Article OMS")

    # chemin
    TEXT_PATH = "data/article_oms.txt"

    try:
        article = load_text(TEXT_PATH)
    except FileNotFoundError:
        st.error(f"Fichier introuvable : {TEXT_PATH}")
        st.stop()
    # Aperçu partiel de l’article
    with st.expander("Aperçu de l’article", expanded=False):
        st.write(article[:1200] + ("..." if len(article) > 1200 else ""))

    # --- Prétraitement
    cleaned = preprocess_text(article)

    # --- Paramètres UI
    st.sidebar.subheader("WordCloud")
    min_len = st.sidebar.slider("Longueur minimale des mots", 2, 8, 3)
    max_words = st.sidebar.slider("Nombre max de mots", 50, 400, 200, step=25)
    background = st.sidebar.selectbox("Fond", ["white", "black"])
    collocations = st.sidebar.checkbox("Autoriser collocations (bigrams)", value=False)

    extra_stopwords = st.sidebar.text_area(
        "Stopwords supplémentaires (séparés par virgules)",
        value="",
        placeholder="ex: santé, mondiale, rapport",
    )

    # Fusion des stopwords par défaut avec ceux ajoutés par l’utilisateur
    stopwords = set(DEFAULT_STOPWORDS_FR)
    if extra_stopwords.strip():
        stopwords |= {w.strip().lower() for w in extra_stopwords.split(",") if w.strip()}

    # Tokenisation + filtrage
    clean_tokens = tokenize_filter(cleaned, stopwords=stopwords, min_len=min_len)
    
    # Indicateurs pour visualiser l’impact du nettoyage
    col1, col2 = st.columns(2)
    col1.metric("Tokens bruts", len(cleaned.split()))
    col2.metric("Tokens nettoyés", len(clean_tokens))

    if not clean_tokens:
        st.warning("Après filtrage, il ne reste aucun mot. Diminue les stopwords ou la longueur minimale.")
        st.stop()

    text_for_wc = " ".join(clean_tokens)

    # --- Génération + affichage
    wc = build_wordcloud(
        text_for_wc=text_for_wc,
        width=1000,
        height=500,
        background=background,
        max_words=max_words,
        collocations=collocations,
    )
    # Affichage
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)

    # Interprétation
    st.subheader("Analyse du nuage de mots")

    st.markdown(
        """
    Le nuage de mots met en évidence les termes les plus fréquents de l'article de l'OMS. 
    On observe notamment la présence de mots liés à la santé mondiale et aux indicateurs sanitaires 
    (par exemple : sante, *progres, deces, sanitaire, oms, etc.).
    Cela confirme que l'article traite principalement du ralentissement des progrès en matière de santé au niveau mondial et des inégalités persistantes entre les régions. 
    Cette analyse textuelle complète donc l'exploration de notre jeu de données de statistiques de santé globale.

    Cette analyse textuelle complète les graphiques et les statistiques de l’application en
    apportant une lecture plus qualitative du contenu du rapport, et permet de mieux
    comprendre le contexte global des données analysées.
    """
    )


    # --- Téléchargement du WordCloud
    png_bytes = wc.to_image()
    # to_image() renvoie une PIL.Image -> on convertit en bytes
    import io
    buf = io.BytesIO()
    png_bytes.save(buf, format="PNG")
    st.download_button(
        "Télécharger le WordCloud (PNG)",
        data=buf.getvalue(),
        file_name="wordcloud_oms.png",
        mime="image/png",
    )
