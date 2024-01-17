import speech_recognition as sr

# Load the audio file
audio_path = '/mnt/data/onlymp3.to - Jaloner Ojitos Prod. Sudakillah -df_F4ZHsdio-192k-1704630184.mp3'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Process the audio file
with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)
    try:
        # Attempt to recognize the speech in the audio
        text = recognizer.recognize_google(audio_data, language='es-ES')
    except sr.UnknownValueError:
        # Speech was unintelligible
        text = "No se pudo entender el audio."
    except sr.RequestError as e:
        # Could not request results from Google Speech Recognition service
        text = f"Error en el servicio de reconocimiento de voz: {e}"

text
