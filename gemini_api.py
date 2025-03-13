import aiohttp
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

if not GEMINI_API_KEY or not GEMINI_API_URL:
    raise ValueError("Missing required environment variables. Please check your .env file.")

async def appeler_gemini_api(texte: str) -> dict:
    """
    Envoie une requête à l'API Gemini et retourne la réponse.
    
    Args:
        texte (str): Le texte à envoyer à l'API, peut inclure le contexte de la conversation
    
    Returns:
        dict: La réponse de l'API
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    # Extraire le contexte de la conversation s'il est présent
    if "Contexte de la conversation précédente:" in texte:
        parts = texte.split("Nouvelle question de l'utilisateur:", 1)
        prompt = parts[1].strip() if len(parts) > 1 else texte
        # Inclure le contexte dans la configuration
        contexte = parts[0].replace("Contexte de la conversation précédente:", "").strip()
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Tu es un assistant vocal français. Voici le contexte de la conversation:\n{contexte}\n\nUtilisateur: {prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }
    else:
        # Sans contexte, utiliser le texte directement
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Tu es un assistant vocal français. Réponds à cette question:\n{texte}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }

    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    resultat = await response.json()
                    return resultat
                else:
                    error_text = await response.text()
                    print(f"Erreur API (Status {response.status}): {error_text}")
                    return {"error": f"Erreur API: {response.status}"}
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API: {str(e)}")
        return {"error": f"Erreur de connexion: {str(e)}"}

async def main():
    # Test avec une question en français
    texte = "Expliquez-moi comment fonctionne l'intelligence artificielle en français."
    print(f"Envoi de la requête: {texte}")
    
    response = await appeler_gemini_api(texte)
    print("\nRéponse de l'API Gemini:")
    print(json.dumps(response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
