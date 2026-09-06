import streamlit as st
import pandas as pd
import requests
import time
import io

st.set_page_config(page_title="Analyse de Prospects", page_icon="📊", layout="centered")

st.title("🤖 Agent Commercial IA - Analyse CSV")
st.subheader("Téléchargez votre fichier et obtenez une analyse enrichie")

with st.sidebar:
    st.header("🔑 Authentification")
    api_key = st.text_input(
        "Entrez votre clé API :",
        type="password",
        placeholder="Ex: demo-key-123 ou votre clé personnelle"
    )
    api_url = st.text_input(
        "URL de l'API :",
        value="https://agent-commercial-ia.onrender.com/analyser"
    )
    st.markdown("---")
    st.caption("Besoin d'une clé ? Contactez-nous pour acheter des crédits.")
    if st.button("🏠 Retour à l'accueil"):
        st.switch_page("streamlit_app.py")

st.markdown("### 📤 Téléchargez votre fichier de prospects")
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
        st.stop()

    col_email = None
    for col in ["email_brut", "message", "contenu", "email", "texte", "mail"]:
        if col in df.columns:
            col_email = col
            break
    if col_email is None:
        st.error("❌ Aucune colonne valide trouvée. Ajoutez 'email_brut' ou 'message'.")
        st.stop()
    st.info(f"📧 Colonne détectée : **{col_email}**")

    if st.button("🚀 Lancer l'analyse", type="primary"):
        if not api_key:
            st.error("Veuillez entrer votre clé API.")
            st.stop()
        resultats = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(df)
        for index, row in df.iterrows():
            status_text.text(f"Analyse {index+1}/{total}...")
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
                    st.stop()
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
    st.info("👈 Téléchargez un fichier CSV pour commencer.")
    st.markdown("""
    **Format attendu :**
    - Une colonne contenant le texte de l'email ou du message.
    - Noms autorisés : `email_brut`, `message`, `contenu`, `email`, `texte`, `mail`.
    """)
st.markdown("---")
st.caption("🔒 Données sécurisées - Aucun stockage.")