import speech_recognition as sr
from text_to_speech_fr import text_to_speech
import asyncio

async def listen_french():
    """
    Écoute et reconnaît la parole en français
    Returns:
        str or None: Le texte reconnu, ou None si erreur
    """
    # Initialize the recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Initialisation du microphone...")
    with microphone as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        print("Dites quelque chose en français...")
        
        try:
            # Listen to the microphone
            audio = recognizer.listen(source)
            print("Traitement de l'audio...")
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous avez dit : " + text)
            return text
            
        except sr.UnknownValueError:
            print("Impossible de comprendre l'audio.")
            await text_to_speech("Je n'ai pas compris ce que vous avez dit. Pouvez-vous répéter ?")
            return None
        except sr.RequestError as e:
            print("Erreur lors de la requête; {0}".format(e))
            await text_to_speech("Désolé, il y a eu une erreur technique. Pouvez-vous réessayer ?")
            return None

async def main():
    await listen_french()

if __name__ == "__main__":
    asyncio.run(main())
