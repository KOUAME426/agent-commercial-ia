import streamlit as st

st.set_page_config(
    page_title="Agent IA Commercial",
    page_icon="🚀",
    layout="wide"
)

# ============================================
# SIDEBAR (Navigation simplifiée)
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/artificial-intelligence.png", width=80)
    st.title("Navigation")
    
    # ICI on est sur la page d'accueil, donc on indique "Accueil" sans lien
    st.markdown("🏠 **Accueil**")
    
    # Lien vers la page d'analyse (avec le bon nom de fichier)
    st.page_link("pages/analyse_csv.py", label="📊 Analyse CSV")
    
    st.divider()
    st.caption("Besoin d'une clé API ?")
    st.caption("Contactez-nous pour un essai gratuit.")

# ============================================
# CONTENU DE LA PAGE D'ACCUEIL
# ============================================
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

# Fonctionnalités
st.divider()
st.subheader("✨ Ce que l'agent IA fait pour vous")
col_feat1, col_feat2, col_feat3 = st.columns(3)
with col_feat1:
    st.markdown("### 🎯 Scoring intelligent")
    st.write("Chaque prospect reçoit une note de 1 à 10 basée sur le budget, l'urgence et l'intention d'achat.")
with col_feat2:
    st.markdown("### 💬 Réponses personnalisées")
    st.write("Fini les réponses génériques. L'IA rédige un brouillon commercial adapté à chaque email.")
with col_feat3:
    st.markdown("### 📊 Export instantané")
    st.write("Téléchargez un fichier CSV enrichi prêt à être importé dans votre CRM.")

# Témoignage
st.divider()
st.subheader("💬 Ce que disent les premiers testeurs")
st.info("""
*"Avant, je perdais 30 min par jour à trier mes emails. Maintenant, l'IA me dit directement qui appeler en premier. C'est un gain de temps phénoménal !"*  
— **Marc D., Dirigeant InnovTech**
""")

# Tarifs
st.divider()
st.subheader("💰 Tarifs simples et transparents")
st.markdown("Aucun abonnement caché. Vous payez uniquement les analyses que vous utilisez.")

col_prix1, col_prix2, col_prix3 = st.columns(3)
with col_prix1:
    st.markdown("### 🆓 Découverte")
    st.markdown("**10 crédits**")
    st.markdown("#### **GRATUIT**")
    st.write("Idéal pour tester la qualité de l'IA.")
    st.page_link("pages/analyse_csv.py", label="S'inscrire gratuitement", use_container_width=True)

with col_prix2:
    st.markdown("### 🚀 Startup")
    st.markdown("**200 crédits**")
    st.markdown("#### **79 €**")
    st.write("Parfait pour un commercial ou une petite équipe.")
    st.button("Contacter pour acheter", key="buy_startup", use_container_width=True, disabled=True)

with col_prix3:
    st.markdown("### 💼 Business")
    st.markdown("**1000 crédits**")
    st.markdown("#### **299 €**")
    st.write("Pour les équipes commerciales et les agences.")
    st.button("Contacter pour acheter", key="buy_business", use_container_width=True, disabled=True)

st.caption("💡 *Le paiement se fait par virement ou PayPal. Les crédits sont valables 1 an.*")

# Footer
st.divider()
col_foot1, col_foot2, col_foot3 = st.columns(3)
with col_foot1:
    st.write("**Agent Commercial IA** v1.0")
with col_foot2:
    st.write("🔒 Données sécurisées - Aucun stockage")
with col_foot3:
    st.write("📧 contact@votre-entreprise.fr")