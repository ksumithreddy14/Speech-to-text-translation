import os
import speech_recognition as sr
from googletrans import Translator
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the Google Translator
translator = Translator()

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Function to record audio using speech_recognition's microphone
def record_audio():
    print("Listening for speech...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Say something...")
        audio = recognizer.listen(source)
        print("Recording complete")
    return audio

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_speech_to_text():
    try:
        # Record the audio using speech_recognition's Microphone
        audio_data = record_audio()

        # Recognize the speech using Google's speech recognition
        print("Attempting to recognize speech...")
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")

            if not text:
                raise ValueError("No speech recognized")

            # Translate the text to Spanish
            print("Attempting to translate text...")
            translated_text = translator.translate(text, src='en', dest='es').text  # Translate to Spanish
            print(f"Translated text: {translated_text}")

            if not translated_text:
                raise ValueError("Translation failed")

            # Return recognized text and translated text
            return jsonify({
                "recognized_text": text,
                "translated_text": translated_text
            })

        except sr.UnknownValueError:
            print("Could not understand the audio")
            return jsonify({"error": "Could not understand the audio"})
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return jsonify({"error": f"Could not request results; {e}"})
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)})

@app.route("/stop", methods=["POST"])
def stop_speech_to_text():
    # Optionally, you could add code to stop listening here if needed
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(debug=True)
