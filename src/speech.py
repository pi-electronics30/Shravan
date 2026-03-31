import pyttsx3
import threading

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.lock = threading.Lock()

    def _speak(self, text):
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def say(self, text):
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()
