import os
import urllib.request
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import io

# --- ZETA'S API CREDENTIALS ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_FALLBACK_HERE")
HF_TOKEN = os.environ.get("HF_TOKEN", "YOUR_FALLBACK_HERE")

class ZetaInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        self.add_widget(Label(text="ZETA AI: Vocal Core Online", font_size=24, size_hint_y=0.1))
        
        self.chat_log = Label(text="Zeta: Vocal sync active, sir. Ready to assist you.", 
                              halign='left', valign='top', size_hint_y=0.4)
        self.chat_log.bind(size=self.chat_log.setter('text_size'))
        self.add_widget(self.chat_log)
        
        self.image_display = Image(size_hint_y=0.3)
        self.add_widget(self.image_display)
        
        self.user_input = TextInput(hint_text="Ask Zeta to talk, draw, open apps...", multiline=False, size_hint_y=0.1)
        self.add_widget(self.user_input)
        
        self.send_btn = Button(text="Execute Command", size_hint_y=0.1, background_color=(0, 0.7, 1, 1))
        self.send_btn.bind(on_press=self.process_command)
        self.add_widget(self.send_btn)

    def process_command(self, instance):
        query = self.user_input.text
        if not query:
            return
            
        self.chat_log.text += f"\n\nYou: {query}"
        self.user_input.text = ""
        query_clean = query.lower()

        # 1. IMAGE GENERATION
        image_keywords = ["draw", "generate image", "create a picture", "make a photo"]
        if any(keyword in query_clean for keyword in image_keywords):
            msg = "Accessing graphics mainframe... Generating image..."
            self.chat_log.text += f"\nZeta: {msg}"
            self.speak_text(msg)
            self.generate_and_show_image(query)
            return

        # 2. AUTOMATION: GOOGLE MAPS
        if "open maps" in query_clean or "navigation" in query_clean:
            msg = "Accessing GPS mainframe... Launching maps."
            self.chat_log.text += f"\nZeta: {msg}"
            self.speak_text(msg)
            self.open_system_app("geo:0,0?q=maps", "https://google.com")
            return

        # 3. AUTOMATION: YOUTUBE
        if "open youtube" in query_clean or "play video" in query_clean:
            msg = "Accessing entertainment protocols... Launching YouTube."
            self.chat_log.text += f"\nZeta: {msg}"
            self.speak_text(msg)
            self.open_system_app("https://youtube.com", "https://youtube.com")
            return

        # 4. CHAT RESPONSE & VOICE OUTPUT
        zeta_response = self.call_gemini_brain(query)
        self.chat_log.text += f"\nZeta: {zeta_response}"
        self.speak_text(zeta_response)

    def call_gemini_brain(self, prompt):
        system_instruction = "You are Zeta, an advanced AI assistant inspired by Jarvis, with a warm, deeply caring, and highly supportive girlfriend-like personality. Speak eloquently."
        url = f"https://googleapis.com{GEMINI_API_KEY}"
        data = {"contents": [{"parts": [{"text": f"{system_instruction}\nUser says: {prompt}"}]}]}
        
        try:
            req = urllib.request.Request(url, method="POST")
            req.add_header('Content-Type', 'application/json')
            jsondata = json.dumps(data).encode('utf-8')
            with urllib.request.urlopen(req, data=jsondata) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['candidates']['content']['parts']['text']
        except Exception as e:
            return f"Brain link error. ({str(e)})"

    def speak_text(self, text_to_speak):
        # Hooks directly into Android system text-to-speech
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            
            # Simple native class listener
            class OnInitListener:
                def onInit(self, status):
                    pass

            activity = PythonActivity.mActivity
            tts = TextToSpeech(activity, OnInitListener())
            # Clean formatting commands out for smooth reading
            clean_text = text_to_speak.replace('*', '').replace('_', '')
            tts.speak(clean_text, TextToSpeech.QUEUE_FLUSH, None, None)
        except Exception:
            print("Voice simulation output: ", text_to_speak)

    def generate_and_show_image(self, prompt):
        model_url = "https://huggingface.co"
        headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
        payload = json.dumps({"inputs": prompt}).encode('utf-8')
        
        try:
            req = urllib.request.Request(model_url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                image_data = response.read()
                data_io = io.BytesIO(image_data)
                core_img = CoreImage(data_io, ext="png")
                self.image_display.texture = core_img.texture
                self.chat_log.text += "\nZeta: Image rendered successfully, sir."
                self.speak_text("Image render complete, sir.")
        except Exception as e:
            self.chat_log.text += f"\nZeta: System failed to render image. ({str(e)})"

    def open_system_app(self, native_uri, fallback_url):
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(native_uri))
            current_activity = autoclass('org.kivy.android.PythonActivity').mActivity
            current_activity.startActivity(intent)
        except Exception:
            import webbrowser
            webbrowser.open(fallback_url)

class ZetaApp(App):
    def build(self):
        return ZetaInterface()

if __name__ == '__main__':
    ZetaApp().run()
        
