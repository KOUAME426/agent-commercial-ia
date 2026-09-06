import streamlit as st
import pandas as pd
import requests
import time
import io

# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================
st.set_page_config(page_title="Agent IA Commercial", page_icon="🚀", layout="wide")

# ============================================================
# DÉFINITION DES PAGES
# ============================================================
def page_accueil():
    """Page d'accueil avec la landing page."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🚀 Gagnez 10h/semaine sur votre prospection")
        st.markdown("### L'IA qui analyse vos emails entrants et rédige des réponses commerciales sur-mesure en 2 secondes.")
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            # Navigation vers la page analyse via le session_state
            if st.button("🔥 Essayer gratuitement", use_container_width=True):
                st.session_state.page = "Analyse"
                st.rerun()
        with col_btn2:
            st.markdown("[📅 Voir la démo](#tarifs)", unsafe_allow_html=True)
    with col2:
        st.image("https://img.icons8.com/fluency/300/null/chatbot.png", caption="Votre assistant commercial 24h/24")

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

    st.divider()
    st.subheader("💬 Ce que disent les premiers testeurs")
    st.info("""
    *"Avant, je perdais 30 min par jour à trier mes emails. Maintenant, l'IA me dit directement qui appeler en premier. C'est un gain de temps phénoménal !"*  
    — **Marc D., Dirigeant InnovTech**
    """)

    st.divider()
    st.subheader("💰 Tarifs simples et transparents")
    st.markdown("Aucun abonnement caché. Vous payez uniquement les analyses que vous utilisez.")
    col_prix1, col_prix2, col_prix3 = st.columns(3)
    with col_prix1:
        st.markdown("### 🆓 Découverte")
        st.markdown("**10 crédits**")
        st.markdown("#### **GRATUIT**")
        st.write("Idéal pour tester la qualité de l'IA.")
        if st.button("S'inscrire gratuitement", key="free", use_container_width=True):
            st.session_state.page = "Analyse"
            st.rerun()
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

    st.divider()
    col_foot1, col_foot2, col_foot3 = st.columns(3)
    with col_foot1:
        st.write("**Agent Commercial IA** v1.0")
    with col_foot2:
        st.write("🔒 Données sécurisées - Aucun stockage")
    with col_foot3:
        st.write("📧 contact@votre-entreprise.fr")


def page_analyse():
    """Page d'analyse CSV (upload, traitement, téléchargement)."""
    st.title("🤖 Agent Commercial IA - Analyse CSV")
    st.subheader("Téléchargez votre fichier et obtenez une analyse enrichie")

    with st.sidebar:
        st.header("🔑 Authentification")
        api_key = st.text_input(
            "Entrez votre clé API :",
            type="password",
            placeholder="Ex: demo-key-123",
            help="Vous avez reçu cette clé par email après votre achat."
        )
        api_url = st.text_input(
            "URL de l'API :",
            value="https://agent-commercial-ia.onrender.com/analyser",
            help="URL de votre serveur API."
        )
        st.markdown("---")
        if st.button("🏠 Retour à l'accueil"):
            st.session_state.page = "Accueil"
            st.rerun()

    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV",
        type=["csv"],
        help="Votre fichier doit contenir une colonne nommée 'email_brut', 'message' ou 'texte'."
    )

    if uploaded_file is not None and api_key:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Fichier chargé : {len(df)} lignes trouvées.")
            st.dataframe(df.head(3))
        except Exception as e:
            st.error(f"Erreur de lecture : {e}")
            return

        col_email = None
        for col in ["email_brut", "message", "contenu", "email", "texte", "mail"]:
            if col in df.columns:
                col_email = col
                break
        if col_email is None:
            st.error("❌ Aucune colonne valide trouvée.")
            return
        st.info(f"📧 Colonne détectée : **{col_email}**")

        if st.button("🚀 Lancer l'analyse des prospects", type="primary"):
            if not api_key:
                st.error("Veuillez entrer votre clé API dans la barre latérale.")
                return

            resultats = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            total = len(df)

            for index, row in df.iterrows():
                status_text.text(f"Analyse du prospect {index+1}/{total}...")
                email_text = str(row[col_email])
                headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
                payload = {"email": email_text}

                try:
                    response = requests.post(api_url, json=payload, headers=headers, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        resultats.append({
                            "nom_prospect": data.get("nom", ""),
                            "entreprise": data.get("entreprise", ""),
                            "score": data.get("score", 0),
                            "motif_interet": data.get("motif_interet", ""),
                            "reponse_proposee": data.get("reponse_proposee", "")
                        })
                    elif response.status_code == 402:
                        st.error("⛔ Crédits épuisés !")
                        return
                    else:
                        resultats.append({
                            "nom_prospect": "Erreur",
                            "entreprise": "",
                            "score": 0,
                            "motif_interet": f"Erreur {response.status_code}",
                            "reponse_proposee": response.text[:100]
                        })
                except Exception as e:
                    resultats.append({
                        "nom_prospect": "Erreur",
                        "entreprise": "",
                        "score": 0,
                        "motif_interet": "Problème réseau",
                        "reponse_proposee": str(e)[:100]
                    })
                progress_bar.progress((index + 1) / total)
                time.sleep(1)

            status_text.text("✅ Analyse terminée !")
            df_resultats = pd.DataFrame(resultats)
            df_final = pd.concat([df, df_resultats], axis=1)
            st.success(f"✅ Analyse terminée ! {len(df_final)} lignes traitées.")
            st.dataframe(df_final.head(5))

            csv_buffer = io.StringIO()
            df_final.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger le fichier enrichi (CSV)",
                data=csv_buffer.getvalue(),
                file_name="prospects_analyses.csv",
                mime="text/csv"
            )

    elif uploaded_file is not None and not api_key:
        st.warning("⚠️ Veuillez entrer votre clé API dans la barre latérale.")
    else:
        st.info("👈 Téléchargez un fichier CSV pour commencer l'analyse.")
        st.markdown("""
        **Format attendu :**
        - Colonne contenant l'email : `email_brut`, `message`, `contenu`, `email`, `texte` ou `mail`.
        """)
    st.caption("🔒 Données sécurisées - Aucun stockage permanent.")


# ============================================================
# NAVIGATION PRINCIPALE (via session_state)
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# Barre latérale de navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/artificial-intelligence.png", width=80)
    st.title("Navigation")
    if st.button("🏠 Accueil"):
        st.session_state.page = "Accueil"
        st.rerun()
    if st.button("📊 Analyse CSV"):
        st.session_state.page = "Analyse"
        st.rerun()
    st.divider()
    st.caption("Besoin d'une clé API ? Contactez-nous.")

# Afficher la page correspondante
if st.session_state.page == "Accueil":
    page_accueil()
else:
    page_analyse()