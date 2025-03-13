import edge_tts
import asyncio
import pygame
import speech_recognition as sr
import threading
import io

class TTSPlayer:
    def __init__(self):
        self.is_playing = False
        self.should_stop = False
        pygame.mixer.init(frequency=24000)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def stop(self):
        self.should_stop = True
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.is_playing = False
        
    def monitor_voice(self):
        """Monitor for voice input to interrupt playback"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while self.is_playing and not self.should_stop:
                try:
                    self.recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                    print("\nInterruption détectée !")
                    self.stop()
                    break
                except sr.WaitTimeoutError:
                    continue
                except Exception:
                    continue

async def text_to_speech(text):
    """
    Convert text to speech using Edge TTS with French voice and play with interruption support
    Args:
        text: Text to convert to speech
    """
    try:
        player = TTSPlayer()
        player.should_stop = False
        player.is_playing = True
        
        # Initialize Edge TTS with French voice
        communicate = edge_tts.Communicate(text, voice="fr-FR-DeniseNeural")
        
        print(f"Génération de l'audio pour : {text}")
        
        # Start voice monitoring in a separate thread
        monitor_thread = threading.Thread(target=player.monitor_voice)
        monitor_thread.start()
        
        # Stream and play audio
        audio_data = io.BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                if player.should_stop:
                    break
                audio_data.write(chunk["data"])
        
        if not player.should_stop:
            try:
                audio_data.seek(0)
                pygame.mixer.music.load(audio_data)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy() and not player.should_stop:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                print(f"Erreur lors de la lecture audio : {str(e)}")
                
        player.is_playing = False
        monitor_thread.join(timeout=1)
            
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale : {str(e)}")
    finally:
        player.stop()
        pygame.mixer.quit()

async def main():
    # Test the TTS with a sample French text
    await text_to_speech("Bonjour, comment puis-je vous aider ?")

if __name__ == "__main__":
    asyncio.run(main())
