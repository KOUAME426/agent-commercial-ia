import os
import json
import hashlib
import time
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================================
# 1. GESTION DES CLIENTS (fichier JSON)
# ============================================
CLIENTS_FILE = "clients.json"

# Structure par défaut si le fichier n'existe pas
def initialiser_clients():
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "w") as f:
            json.dump({
                "client_demo": {
                    "nom": "Client Démo",
                    "cle_api": "demo-key-123",
                    "credits": 10,          # Nombre d'analyses restantes
                    "total_utilise": 0
                }
            }, f, indent=2)

initialiser_clients()

def get_client_info(api_key: str):
    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)
    for client_id, info in data.items():
        if info["cle_api"] == api_key:
            return client_id, info
    return None, None

def update_client_credits(client_id: str, credits_restants: int):
    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)
    data[client_id]["credits"] = credits_restants
    data[client_id]["total_utilise"] += 1
    with open(CLIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ============================================
# 2. MODÈLES DE DONNÉES
# ============================================
class EmailInput(BaseModel):
    email: str

class AnalyseOutput(BaseModel):
    nom: str
    entreprise: str
    score: int
    motif_interet: str
    reponse_proposee: str

class ClientInfo(BaseModel):
    client_nom: str
    credits_restants: int

# ============================================
# 3. APPLICATION FASTAPI
# ============================================
app = FastAPI(title="Agent Commercial IA - API Sécurisée")

# ============================================
# 4. FONCTION CŒUR (analyse)
# ============================================
def analyser_email(email_brut: str) -> dict:
    prompt = f"""
    Tu es un assistant commercial expert. Analyse cet email de prospect :
    ---
    {email_brut}
    ---
    Réponds UNIQUEMENT en format JSON avec ces 5 champs :
    {{
        "nom": "...",
        "entreprise": "...",
        "score": (note de 1 à 10),
        "motif_interet": "...",
        "reponse_proposee": "..."
    }}
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {
            "nom": "Erreur",
            "entreprise": "Erreur",
            "score": 0,
            "motif_interet": f"Erreur : {str(e)}",
            "reponse_proposee": "Impossible d'analyser."
        }

# ============================================
# 5. ENDPOINT PRINCIPAL (avec clé API)
# ============================================
@app.post("/analyser", response_model=AnalyseOutput)
async def analyser_prospect(
    data: EmailInput,
    x_api_key: str = Header(..., description="Votre clé API personnelle")
):
    # Vérifier la clé
    client_id, client_info = get_client_info(x_api_key)
    if not client_id:
        raise HTTPException(status_code=401, detail="Clé API invalide.")
    
    # Vérifier les crédits
    if client_info["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Crédits épuisés. Veuillez recharger.")
    
    # Vérifier l'email
    if not data.email or len(data.email) < 10:
        raise HTTPException(status_code=400, detail="Email trop court (min 10 caractères).")
    
    # Appel à l'agent
    resultat = analyser_email(data.email)
    
    # Déduire un crédit
    update_client_credits(client_id, client_info["credits"] - 1)
    
    # Retourner le résultat
    return resultat

# ============================================
# 6. ENDPOINT POUR CONSULTER SES CRÉDITS
# ============================================
@app.get("/mon-compte", response_model=ClientInfo)
async def mes_infos(x_api_key: str = Header(...)):
    _, info = get_client_info(x_api_key)
    if not info:
        raise HTTPException(status_code=401, detail="Clé API invalide.")
    return ClientInfo(
        client_nom=info["nom"],
        credits_restants=info["credits"]
    )

# ============================================
# 7. ENDPOINT DE SANTÉ (public)
# ============================================
@app.get("/")
async def root():
    return {"message": "API Agent Commercial - Sécurisée", "status": "ok"}

# ============================================
# 8. LANCEMENT (si exécuté directement)
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)