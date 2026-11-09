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
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY_HERE")
HF_TOKEN = os.environ.get("HF_TOKEN", "YOUR_FALLBACK_HERE")

class ZetaInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        # System Banner
        self.add_widget(Label(text="ZETA AI: Multimodal Active", font_size=24, size_hint_y=0.1))
        
        # Chat display area
        self.chat_log = Label(text="Zeta: System online. Ready to chat or generate imagery, sir.", 
                              halign='left', valign='top', size_hint_y=0.4)
        self.chat_log.bind(size=self.chat_log.setter('text_size'))
        self.add_widget(self.chat_log)
        
        # Container to hold generated images dynamically
        self.image_display = Image(size_hint_y=0.3)
        self.add_widget(self.image_display)
        
        # Input Text Box
        self.user_input = TextInput(hint_text="Ask Zeta to chat or draw something...", multiline=False, size_hint_y=0.1)
        self.add_widget(self.user_input)
        
        # Action Button
        self.send_btn = Button(text="Execute Command", size_hint_y=0.1, background_color=(0, 0.7, 1, 1))
        self.send_btn.bind(on_press=self.process_command)
        self.add_widget(self.send_btn)

    def process_command(self, instance):
        query = self.user_input.text
        if not query:
            return
            
        self.chat_log.text += f"\n\nYou: {query}"
        self.user_input.text = ""
        
        # Check if the user is asking for an image
        image_keywords = ["draw", "generate image", "create a picture", "make a photo", "generate picture"]
        if any(keyword in query.lower() for keyword in image_keywords):
            self.chat_log.text += "\nZeta: Accessing graphics mainframe... Generating image..."
            self.generate_and_show_image(query)
            return

        # Direct app control backup check
        if "open maps" in query.lower() or "navigation" in query.lower():
            self.chat_log.text += "\nZeta: Opening coordinates on system maps..."
            self.open_google_maps()
            return

        # Otherwise, fall back to default conversation mode
        zeta_response = self.call_gemini_brain(query)
        self.chat_log.text += f"\nZeta: {zeta_response}"

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

    def generate_and_show_image(self, prompt):
        # We target a highly capable free text-to-image API model endpoint on Hugging Face
        model_url = "https://huggingface.co"
        headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
        payload = json.dumps({"inputs": prompt}).encode('utf-8')
        
        try:
            req = urllib.request.Request(model_url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                image_data = response.read()
                
                # Load the raw image bytes into the Kivy UI elements instantly without saving a local file
                data_io = io.BytesIO(image_data)
                ext = "png"
                core_img = CoreImage(data_io, ext=ext)
                self.image_display.texture = core_img.texture
                self.chat_log.text += "\nZeta: Image rendered successfully, sir."
        except Exception as e:
            self.chat_log.text += f"\nZeta: System failed to render image. ({str(e)})"

    def open_google_maps(self):
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=maps"))
            current_activity = autoclass('org.kivy.android.PythonActivity').mActivity
            current_activity.startActivity(intent)
        except Exception:
            import webbrowser
            webbrowser.open("https://google.com")

class ZetaApp(App):
    def build(self):
        return ZetaInterface()

if __name__ == '__main__':
    ZetaApp().run()
        
