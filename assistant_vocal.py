import asyncio
import speech_recognition as sr
from speech_recognition_fr import listen_french
from text_to_speech_fr import text_to_speech
from gemini_api import appeler_gemini_api
import re

class Assistant:
    def __init__(self):
        self.conversation_history = []
        
    def ajouter_a_historique(self, role, contenu):
        """Ajoute un message à l'historique de conversation"""
        self.conversation_history.append({"role": role, "content": contenu})
        # Garder uniquement les 5 derniers échanges pour maintenir un contexte pertinent
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
            
    def construire_prompt(self, nouveau_message):
        """Construit le prompt en incluant le contexte de la conversation"""
        contexte = "\n".join([
            f"{'Assistant' if msg['role'] == 'assistant' else 'Utilisateur'}: {msg['content']}"
            for msg in self.conversation_history[-4:]  # Utiliser les 4 derniers messages comme contexte
        ])
        
        prompt = f"""Contexte de la conversation précédente:
{contexte}

Nouvelle question de l'utilisateur: {nouveau_message}

Réponds en français, en tenant compte du contexte de la conversation."""
        
        return prompt

def nettoyer_markdown(texte):
    """
    Nettoie le texte markdown pour la synthèse vocale.
    """
    # Supprimer les astérisques de mise en forme
    texte = re.sub(r'\*{1,2}', '', texte)
    
    # Supprimer les points des listes à puces
    texte = re.sub(r'^\s*\*\s+', '', texte, flags=re.MULTILINE)
    
    # Supprimer les crochets et parenthèses des liens
    texte = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', texte)
    
    # Supprimer les retours à la ligne multiples
    texte = re.sub(r'\n\s*\n', '\n', texte)
    
    # Supprimer les backticks de code
    texte = re.sub(r'`[^`]+`', '', texte)
    
    # Remplacer les virgules par des pauses
    texte = texte.replace(',', ', ')
    
    # Nettoyer la ponctuation excessive
    texte = re.sub(r'([.!?])\s*([.!?])+', r'\1', texte)
    
    return texte.strip()

async def assistant_vocal():
    """
    Assistant vocal qui:
    1. Écoute l'entrée vocale en français
    2. Envoie le texte à l'API Gemini avec le contexte
    3. Convertit la réponse en voix
    """
    assistant = Assistant()
    print("=== Assistant Vocal Français ===")
    print("(Vous pouvez parler pendant la réponse pour l'interrompre)")
    
    while True:
        try:
            # 1. Reconnaissance vocale
            print("\nÉcoute...")
            texte_recu = await listen_french()
            
            if texte_recu is None:
                continue
                
            print(f"\nTexte reconnu: {texte_recu}")
            
            # Vérifier si l'utilisateur veut arrêter
            if texte_recu.lower() in ["arrêter", "stop", "quitter", "au revoir"]:
                await text_to_speech("Au revoir !")
                print("Au revoir !")
                break
            
            # Ajouter l'entrée utilisateur à l'historique
            assistant.ajouter_a_historique("user", texte_recu)
            
            # 2. Appel à l'API Gemini avec contexte
            print("Traitement de la demande...")
            prompt_avec_contexte = assistant.construire_prompt(texte_recu)
            reponse = await appeler_gemini_api(prompt_avec_contexte)
            
            # Extraction du texte de la réponse
            if "error" in reponse:
                texte_reponse = "Désolé, je n'ai pas pu traiter votre demande."
            else:
                try:
                    texte_reponse = reponse.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if not texte_reponse:
                        texte_reponse = "Désolé, je n'ai pas pu générer une réponse appropriée."
                    else:
                        # Nettoyer le markdown avant la synthèse vocale
                        texte_reponse = nettoyer_markdown(texte_reponse)
                except (KeyError, IndexError):
                    texte_reponse = "Désolé, la réponse n'est pas dans le format attendu."
            
            # Ajouter la réponse à l'historique
            assistant.ajouter_a_historique("assistant", texte_reponse)
            
            print(f"\nRéponse: {texte_reponse}")
            
            # 3. Synthèse vocale avec possibilité d'interruption
            print("\nGénération de la réponse vocale...")
            await text_to_speech(texte_reponse)
            
            # Message pour continuer
            print("\nDites quelque chose ou 'arrêter' pour quitter...")
                
        except Exception as e:
            print(f"Erreur: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(assistant_vocal())
