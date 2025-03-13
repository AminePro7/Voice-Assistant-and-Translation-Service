import asyncio
import speech_recognition as sr
from speech_recognition_fr import listen_french
from text_to_speech_fr import text_to_speech
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import pygame
import time

class TranslatorAssistant:
    def __init__(self, target_lang):
        self.translator = Translator()
        self.target_lang = target_lang
        
    async def translate_text(self, text):
        """Translate text from French to target language"""
        try:
            translation = self.translator.translate(text, src='fr', dest=self.target_lang)
            return translation.text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None

    async def text_to_speech_target(self, text):
        """Convert text to speech in target language"""
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name

            # Generate speech in target language
            tts = gTTS(text=text, lang=self.target_lang)
            tts.save(temp_filename)
            
            try:
                # Initialize pygame mixer before each playback
                pygame.mixer.quit()
                pygame.mixer.init()
                
                # Load and play the audio
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                # Wait for the audio to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                # Clean up pygame mixer
                pygame.mixer.quit()
                
            except Exception as e:
                print(f"Audio playback error: {str(e)}")
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_filename)
                except:
                    pass
                
        except Exception as e:
            print(f"Text-to-speech error: {str(e)}")

def get_language_selection():
    """Get target language selection from user"""
    languages = {
        '1': ('English', 'en'),
        '2': ('Spanish', 'es'),
        '3': ('German', 'de'),
        '4': ('Italian', 'it'),
        '5': ('Portuguese', 'pt'),
        '6': ('Arabic', 'ar'),
        '7': ('Chinese', 'zh-cn'),
        '8': ('Japanese', 'ja'),
        '9': ('Korean', 'ko'),
        '10': ('Russian', 'ru')
    }
    
    print("\n=== Available Languages ===")
    for key, (name, code) in languages.items():
        print(f"{key}: {name}")
    
    while True:
        choice = input("\nSelect target language number (1-10): ")
        if choice in languages:
            return languages[choice][1]
        print("Invalid selection. Please try again.")

async def translator_service():
    """
    Translator service that:
    1. Gets target language selection
    2. Listens for French speech input
    3. Translates to target language
    4. Converts translation to speech
    """
    # Get target language
    target_lang = get_language_selection()
    translator = TranslatorAssistant(target_lang)
    
    print("\n=== French to", target_lang.upper(), "Translator ===")
    print("(Speak in French, say 'arrêter' to quit)")
    
    while True:
        try:
            # 1. Speech recognition
            print("\nListening for French...")
            text_received = await listen_french()
            
            if text_received is None:
                continue
                
            print(f"\nRecognized French text: {text_received}")
            
            # Check if user wants to stop
            if text_received.lower() in ["arrêter", "stop", "quitter", "au revoir"]:
                await text_to_speech("Au revoir !")
                print("Goodbye!")
                break
            
            # 2. Translation
            print(f"\nTranslating to {target_lang}...")
            translated_text = await translator.translate_text(text_received)
            
            if translated_text:
                print(f"\nTranslation: {translated_text}")
                
                # 3. Text to speech in target language
                print("\nGenerating speech...")
                await translator.text_to_speech_target(translated_text)
            
            print("\nSpeak something in French or say 'arrêter' to quit...")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            continue

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    try:
        asyncio.run(translator_service())
    finally:
        # Clean up pygame
        pygame.quit()