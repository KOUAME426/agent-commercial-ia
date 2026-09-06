import streamlit as st
import pandas as pd
import requests
import time
import io

# ============================================
# 1. CONFIGURATION DE LA PAGE
# ============================================
st.set_page_config(
    page_title="Agent IA - Analyse de Prospects",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Agent Commercial IA")
st.subheader("Analysez automatiquement vos prospects en un clic")

# ============================================
# 2. SIDEBAR : SAISIE DE LA CLÉ API
# ============================================
with st.sidebar:
    st.header("🔑 Authentification")
    api_key = st.text_input(
        "Entrez votre clé API :",
        type="password",
        placeholder="Ex: demo-key-123 ou votre clé personnelle",
        help="Vous avez reçu cette clé par email après votre achat."
    )
    
    # URL de votre API (à modifier si vous déployez ailleurs)
    api_url = st.text_input(
        "URL de l'API :",
        value="https://agent-commercial-ia.onrender.com/analyser",
        help="URL de votre serveur API."
    )
    
    st.markdown("---")
    st.caption("Besoin d'une clé ? Contactez-nous pour acheter des crédits.")

# ============================================
# 3. UPLOAD DU FICHIER CSV
# ============================================
st.markdown("### 📤 Téléchargez votre fichier de prospects")

uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV",
    type=["csv"],
    help="Votre fichier doit contenir une colonne nommée 'email_brut', 'message' ou 'texte'."
)

# ============================================
# 4. TRAITEMENT AUTOMATIQUE
# ============================================
if uploaded_file is not None and api_key:
    # Lire le CSV
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Fichier chargé avec succès : {len(df)} lignes trouvées.")
        st.dataframe(df.head(3))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        st.stop()

    # Vérifier la colonne contenant les emails
    col_email = None
    for col in ["email_brut", "message", "contenu", "email", "texte", "mail"]:
        if col in df.columns:
            col_email = col
            break
    
    if col_email is None:
        st.error("❌ Aucune colonne valide trouvée. Ajoutez une colonne nommée 'email_brut' ou 'message'.")
        st.stop()
    
    st.info(f"📧 Colonne détectée : **{col_email}** (utilisée comme texte des prospects)")

    # Bouton pour lancer le traitement
    if st.button("🚀 Lancer l'analyse des prospects", type="primary"):
        if not api_key:
            st.error("Veuillez entrer votre clé API dans la barre latérale.")
            st.stop()
        
        # Préparer les résultats
        resultats = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total = len(df)
        
        for index, row in df.iterrows():
            status_text.text(f"Analyse du prospect {index+1}/{total}...")
            
            # Préparer la requête
            email_text = str(row[col_email])
            headers = {
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            }
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
                    st.error("⛔ Crédits épuisés ! Veuillez recharger votre compte.")
                    st.stop()
                else:
                    resultats.append({
                        "nom_prospect": "Erreur",
                        "entreprise": "Erreur",
                        "score": 0,
                        "motif_interet": f"Erreur {response.status_code}",
                        "reponse_proposee": response.text[:100]
                    })
            except requests.exceptions.RequestException as e:
                resultats.append({
                    "nom_prospect": "Erreur",
                    "entreprise": "Erreur",
                    "score": 0,
                    "motif_interet": "Problème réseau",
                    "reponse_proposee": str(e)[:100]
                })
            
            # Mettre à jour la progression
            progress_bar.progress((index + 1) / total)
            # Pause pour respecter les limites de l'API (optionnel)
            time.sleep(1)
        
        status_text.text("✅ Analyse terminée !")
        
        # Fusionner les résultats avec le DataFrame original
        df_resultats = pd.DataFrame(resultats)
        df_final = pd.concat([df, df_resultats], axis=1)
        
        # Afficher l'aperçu
        st.success(f"✅ Analyse terminée avec succès ! {len(df_final)} lignes traitées.")
        st.dataframe(df_final.head(5))
        
        # Bouton de téléchargement
        csv_buffer = io.StringIO()
        df_final.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Télécharger le fichier enrichi (CSV)",
            data=csv_data,
            file_name="prospects_analyses.csv",
            mime="text/csv"
        )

elif uploaded_file is not None and not api_key:
    st.warning("⚠️ Veuillez entrer votre clé API dans la barre latérale pour commencer.")

else:
    st.info("👈 Commencez par télécharger un fichier CSV dans la zone ci-dessus.")
    st.markdown("""
    **Format attendu :**
    - Une colonne contenant le texte de l'email ou du message.
    - Noms autorisés : `email_brut`, `message`, `contenu`, `email`, `texte`, `mail`.
    - Exemple : 
    
    | email_brut |
    |------------|
    | "Bonjour, je suis Paul..." |
    | "Salut, j'ai un budget..." |
    """)

# ============================================
# 5. PIED DE PAGE (footer)
# ============================================
st.markdown("---")
st.caption("🔒 Toutes les communications sont sécurisées. Vos données ne sont pas stockées sur nos serveurs.")