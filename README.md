# 🎙️ Voice Assistant and Translation Service 🌐

A powerful Python-based voice assistant that combines AI-powered responses with real-time translation capabilities. The project consists of two main components: a French voice assistant using Google's Gemini AI and a multi-language translation service.

## ✨ Features

### 1. 🗣️ Voice Assistant (assistant_vocal.py)
- 🎯 French voice recognition and text-to-speech
- 🤖 AI-powered responses using Google's Gemini API
- 💭 Context-aware conversations (maintains conversation history)
- 📝 Markdown text cleaning for natural speech
- ⏹️ Interruptible responses
- 🔄 Natural conversation flow with context retention

### 2. 🌍 Translation Service (translator_assistant.py)
- 🎙️ Real-time French speech to text conversion
- 🔄 Translation to multiple languages:
  - 🇬🇧 English (en)
  - 🇪🇸 Spanish (es)
  - 🇩🇪 German (de)
  - 🇮🇹 Italian (it)
  - 🇵🇹 Portuguese (pt)
  - 🇸🇦 Arabic (ar)
  - 🇨🇳 Chinese (zh-cn)
  - 🇯🇵 Japanese (ja)
  - 🇰🇷 Korean (ko)
  - 🇷🇺 Russian (ru)
- 🔊 Text-to-speech in target language
- 🎯 Interactive language selection
- 🎵 Seamless audio playback

## 📋 Prerequisites

- 🐍 Python 3.7+
- 🎤 Microphone
- 🔊 Speakers/Headphones
- 🌐 Internet connection

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/AminePro7/Voice-Assistant-and-Translation-Service.git
cd Voice-Assistant-and-Translation-Service
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
```

## 💡 Usage

### 🗣️ Voice Assistant
Run the voice assistant:
```bash
python assistant_vocal.py
```
- 🗣️ Speak in French to interact with the AI
- 🛑 Say "arrêter", "stop", "quitter", or "au revoir" to exit
- ⏹️ You can interrupt the assistant's response by speaking

### 🌍 Translation Service
Run the translation service:
```bash
python translator_assistant.py
```
1. 🎯 Select your target language from the menu (1-10)
2. 🗣️ Speak in French
3. The service will:
   - 📝 Convert your speech to text
   - 🔄 Translate it to the selected language
   - 🔊 Play the translated audio
4. 🛑 Say "arrêter" to quit

## 📁 Project Structure

- `assistant_vocal.py`: Main voice assistant implementation
- `translator_assistant.py`: Translation service implementation
- `gemini_api.py`: Gemini API integration
- `speech_recognition_fr.py`: French speech recognition
- `text_to_speech_fr.py`: French text-to-speech
- `.env`: Environment variables (API keys)
- `requirements.txt`: Project dependencies

## 📦 Dependencies

- 🔄 aiohttp: Async HTTP client
- 🔑 python-dotenv: Environment variable management
- 🎙️ SpeechRecognition: Speech recognition
- 🌐 googletrans: Translation service
- 🔊 gTTS: Google Text-to-Speech
- 🎵 pygame: Audio playback

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 