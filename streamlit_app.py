import streamlit as st

# ============================================
# CONFIGURATION DE LA PAGE (MODE LARGE)
# ============================================
st.set_page_config(
    page_title="Agent IA Commercial",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SIDEBAR (Menu de navigation)
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/artificial-intelligence.png", width=80)
    st.title("Navigation")
    
    # Lien vers la page d'analyse (via le nom de la page)
    st.page_link("streamlit_app.py", label="🏠 Accueil", icon="🏠")
    st.page_link("pages/1_📊_Analyse_CSV.py", label="📊 Analyse CSV", icon="📊")
    
    st.divider()
    st.caption("Besoin d'une clé API ?")
    st.caption("Contactez-nous pour un essai gratuit.")

# ============================================
# PAGE D'ACCUEIL (LANDING PAGE)
# ============================================
# 1. HEADER PRINCIPAL
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🚀 Gagnez 10h/semaine sur votre prospection")
    st.markdown("### L'IA qui analyse vos emails entrants et rédige des réponses commerciales sur-mesure en 2 secondes.")
    st.markdown("---")
    
    # Boutons CTA
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.page_link("pages/1_📊_Analyse_CSV.py", label="🔥 Essayer gratuitement", use_container_width=True)
    with col_btn2:
        st.markdown("[📅 Voir la démo](#tarifs)", unsafe_allow_html=True)

with col2:
    st.image("https://img.icons8.com/fluency/300/null/chatbot.png", caption="Votre assistant commercial 24h/24")

# 2. FONCTIONNALITÉS (3 colonnes)
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

# 3. TÉMOIGNAGE / PREUVE SOCIALE
st.divider()
st.subheader("💬 Ce que disent les premiers testeurs")
st.info("""
*"Avant, je perdais 30 min par jour à trier mes emails. Maintenant, l'IA me dit directement qui appeler en premier. C'est un gain de temps phénoménal !"*  
— **Marc D., Dirigeant InnovTech**
""")

# 4. TARIFS (LE CŒUR DE LA PAGE)
st.divider()
st.subheader("💰 Tarifs simples et transparents")
st.markdown("Aucun abonnement caché. Vous payez uniquement les analyses que vous utilisez.")

col_prix1, col_prix2, col_prix3 = st.columns(3)

with col_prix1:
    st.markdown("### 🆓 Découverte")
    st.markdown("**10 crédits**")
    st.markdown("#### **GRATUIT**")
    st.write("Idéal pour tester la qualité de l'IA.")
    st.page_link("pages/1_📊_Analyse_CSV.py", label="S'inscrire gratuitement", use_container_width=True)

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

# Note explicative
st.caption("💡 *Le paiement se fait par virement ou PayPal. Les crédits sont valables 1 an.*")

# 5. FOOTER
st.divider()
col_foot1, col_foot2, col_foot3 = st.columns(3)
with col_foot1:
    st.write("**Agent Commercial IA** v1.0")
with col_foot2:
    st.write("🔒 Données sécurisées - Aucun stockage")
with col_foot3:
    st.write("📧 contact@votre-entreprise.fr (Remplacez par votre email)")