import streamlit as st

st.set_page_config(page_title="Agent IA Commercial", page_icon="🚀", layout="wide")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/artificial-intelligence.png", width=80)
    st.title("Navigation")
    st.markdown("🏠 **Accueil**")
    # Utiliser st.page_link à la place de st.switch_page
    st.page_link("pages/analyse_csv.py", label="📊 Analyse CSV")
    st.divider()
    st.caption("Besoin d'une clé API ? Contactez-nous.")

# Contenu de la page d'accueil
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🚀 Gagnez 10h/semaine sur votre prospection")
    st.markdown("### L'IA qui analyse vos emails entrants et rédige des réponses commerciales sur-mesure en 2 secondes.")
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.page_link("pages/analyse_csv.py", label="🔥 Essayer gratuitement", use_container_width=True)
    with col_btn2:
        st.markdown("[📅 Voir la démo](#tarifs)", unsafe_allow_html=True)

with col2:
    st.image("https://img.icons8.com/fluency/300/null/chatbot.png", caption="Votre assistant commercial 24h/24")

# ... le reste du code (fonctionnalités, témoignages, tarifs) reste identique à avant