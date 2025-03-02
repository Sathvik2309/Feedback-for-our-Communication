import os
import random
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

# List of improvement instructions
improvement_instructions = [
    "Try to speak more clearly.",
    "Maintain a steady pace while speaking.",
    "Work on your pronunciation of difficult words.",
    "Use a more confident tone.",
    "Practice intonation and inflection.",
    "Minimize filler words like 'um' and 'uh'.",
    "Ensure proper breathing while speaking.",
    "Vary your pitch for better engagement.",
    "Keep your voice at a consistent volume.",
    "Make eye contact if speaking to an audience.",
    "Record and listen to yourself for self-improvement.",
    "Practice with a friend for feedback.",
    "Read aloud daily to enhance fluency.",
    "Use pauses effectively to emphasize points.",
    "Avoid speaking too fast; it's okay to take your time.",
    "Engage your audience with questions.",
    "Use gestures to emphasize your points.",
    "Be aware of your body language.",
    "Practice public speaking in front of a mirror.",
    "Take deep breaths to calm your nerves before speaking.",
]

@app.route('/')
def index():
    return render_template('commfee.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = "voice.webm"
    file.save(file_path)  # Save the uploaded file

    # Convert webm to wav using pydub
    wav_path = "voice.wav"
    AudioSegment.from_file(file_path).export(wav_path, format="wav")

    # Use SpeechRecognition to recognize the audio
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

            # Simulate voice quality analysis
            rating = random.randint(1, 5)  # Random rating between 1 to 5
            voice_quality = "Good" if rating >= 4 else "Average" if rating == 3 else "Poor"
            detailed_feedback = f"Voice Quality: {voice_quality} ({rating}/5)"

            # Select random improvement instructions
            improvement = random.sample(improvement_instructions, 3)  
            
            return jsonify({
                "text": text,
                "feedback": f"Your voice quality is {voice_quality}.",  # Updated feedback
                "detailed_feedback": detailed_feedback,
                "improvement_instructions": improvement
            })

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results; {e}"}), 500
    finally:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

if __name__ == '__main__':
    app.run(debug=True)
