import os
import json
import secrets
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
ADMIN_KEY = "admin-secret-2026"  # 🔑 Changez ce mot de passe ! (à garder secret)

def initialiser_clients():
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "w") as f:
            json.dump({
                "client_demo": {
                    "nom": "Client Démo",
                    "cle_api": "demo-key-123",
                    "credits": 10,
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
    if client_id in data:
        data[client_id]["credits"] = credits_restants
        data[client_id]["total_utilise"] += 1
        with open(CLIENTS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    return False

def add_client(nom: str, credits_initial: int = 0) -> dict:
    """Ajoute un nouveau client avec une clé API générée aléatoirement."""
    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)
    
    # Générer une clé API unique
    cle_api = secrets.token_urlsafe(32)  # Ex: "fK9sL2mN8xQ4..."
    
    client_id = f"client_{len(data) + 1}"
    data[client_id] = {
        "nom": nom,
        "cle_api": cle_api,
        "credits": credits_initial,
        "total_utilise": 0
    }
    
    with open(CLIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    return {
        "client_id": client_id,
        "nom": nom,
        "cle_api": cle_api,
        "credits": credits_initial
    }

# ============================================
# 2. MODÈLES DE DONNÉES (Pydantic)
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

class AdminAddCredits(BaseModel):
    client_id: str
    credits_a_ajouter: int

class AdminNewClient(BaseModel):
    nom_client: str
    credits_initiaux: int = 0

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
# 5. ENDPOINT PRINCIPAL (pour les clients)
# ============================================
@app.post("/analyser", response_model=AnalyseOutput)
async def analyser_prospect(
    data: EmailInput,
    x_api_key: str = Header(..., description="Votre clé API personnelle")
):
    client_id, client_info = get_client_info(x_api_key)
    if not client_id:
        raise HTTPException(status_code=401, detail="Clé API invalide.")
    
    if client_info["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Crédits épuisés. Veuillez recharger.")
    
    if not data.email or len(data.email) < 10:
        raise HTTPException(status_code=400, detail="Email trop court (min 10 caractères).")
    
    resultat = analyser_email(data.email)
    update_client_credits(client_id, client_info["credits"] - 1)
    return resultat

# ============================================
# 6. ENDPOINT POUR CONSULTER SES CRÉDITS (client)
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
# 7. ADMIN : LISTER TOUS LES CLIENTS
# ============================================
@app.get("/admin/clients")
async def admin_list_clients(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Accès admin refusé.")
    
    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)
    
    # On cache les clés API pour plus de sécurité (sauf si vous voulez les voir)
    resultat = {}
    for client_id, info in data.items():
        resultat[client_id] = {
            "nom": info["nom"],
            "credits": info["credits"],
            "total_utilise": info["total_utilise"],
            "cle_api": info["cle_api"]  # Si vous voulez voir les clés
        }
    return resultat

# ============================================
# 8. ADMIN : AJOUTER DES CRÉDITS
# ============================================
@app.post("/admin/ajouter-credits")
async def admin_add_credits(
    data: AdminAddCredits,
    x_admin_key: str = Header(...)
):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Accès admin refusé.")
    
    with open(CLIENTS_FILE, "r") as f:
        clients = json.load(f)
    
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="Client introuvable.")
    
    clients[data.client_id]["credits"] += data.credits_a_ajouter
    
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f, indent=2)
    
    return {
        "message": "Crédits ajoutés avec succès.",
        "client_id": data.client_id,
        "nouveaux_credits": clients[data.client_id]["credits"]
    }

# ============================================
# 9. ADMIN : CRÉER UN NOUVEAU CLIENT
# ============================================
@app.post("/admin/nouveau-client")
async def admin_new_client(
    data: AdminNewClient,
    x_admin_key: str = Header(...)
):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Accès admin refusé.")
    
    nouveau = add_client(data.nom_client, data.credits_initiaux)
    return {
        "message": "Client créé avec succès.",
        "client": nouveau
    }

# ============================================
# 10. ADMIN : STATISTIQUES GLOBALES
# ============================================
@app.get("/admin/stats")
async def admin_stats(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Accès admin refusé.")
    
    with open(CLIENTS_FILE, "r") as f:
        data = json.load(f)
    
    total_credits = sum(info["credits"] for info in data.values())
    total_analyses = sum(info["total_utilise"] for info in data.values())
    nombre_clients = len(data)
    
    return {
        "nombre_clients": nombre_clients,
        "total_credits_restants": total_credits,
        "total_analyses_effectuees": total_analyses
    }

# ============================================
# 11. ENDPOINT DE SANTÉ (public)
# ============================================
@app.get("/")
async def root():
    return {"message": "API Agent Commercial - Sécurisée", "status": "ok"}

# ============================================
# 12. LANCEMENT
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)