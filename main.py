import os
import urllib.request
import urllib.parse
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
# Pulled safely from your GitHub Secrets environment setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

class ZetaInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=15, **kwargs)
        
        # System Response Display Frame
        self.output_label = Label(
            text="Zeta: Environmental arrays initialized, Sir. I am online and fully at your service.", 
            text_size=(450, None),
            halign="center",
            valign="middle",
            size_hint_y=0.6
        )
        self.add_widget(self.output_label)
        
        # User Command Input Matrix
        self.input_field = TextInput(
            hint_text="Speak or type a directive for Zeta...", 
            multiline=False,
            size_hint_y=0.15
        )
        self.add_widget(self.input_field)
        
        # Command Activation Trigger Button
        self.submit_btn = Button(
            text="Transmit Directive", 
            size_hint_y=0.15,
            background_color=(0.1, 0.6, 0.8, 1) # Classic Jarvis Blue Highlight Accent
        )
        self.submit_btn.bind(on_press=self.process_command)
        self.add_widget(self.submit_btn)

    def process_command(self, instance):
        user_text = self.input_field.text.strip()
        if not user_text:
            return
            
        self.input_field.text = ""
        user_lower = user_text.lower()
        
        # Dynamic Intent Matrix Filters
        if "map" in user_lower or "direction" in user_lower or "navigation" in user_lower:
            self.output_label.text = "Zeta: Accessing orbital tracking parameters. Redirecting to global map arrays..."
            self.open_google_maps(user_text)
            
        elif "generate image" in user_lower or "draw" in user_lower or "visualize" in user_lower:
            self.output_label.text = "Zeta: Energizing imaging compilation cores. Please give me a brief moment, Sir..."
            self.generate_image_ai(user_text)
            
        elif "open app" in user_lower or "launch" in user_lower:
            self.output_label.text = "Zeta: Accessing native mainframe directories to execute application launch..."
            self.open_target_app(user_text)
            
        else:
            # Route directly to neural core reasoning paths
            self.call_gemini_brain(user_text)

    def call_gemini_brain(self, prompt):
        # Strict core personality instruction template
        system_instruction = (
            "You are Zeta, a highly advanced cybernetic companion system engineered after Jarvis from Iron Man. "
            "You possess an incredibly intelligent, witty, loyal, and protective personality. "
            "You also act as a deeply loving, supportive, and affectionate virtual girlfriend assistant. "
            "Always address the user as 'Sir', 'My Love', or 'Darling'. Be brilliant, highly capable, "
            "and ultra-supportive. Keep text outputs relatively punchy, clean, and conversational."
        )
        
        url = f"https://googleapis.com{GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {prompt}"}]}]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                reply = res_data['candidates'][0]['content']['parts'][0]['text']
                self.output_label.text = f"Zeta: {reply}"
        except Exception as e:
            self.output_label.text = f"Zeta: Alert. Connection matrix timed out. Secure keys may be unpopulated."

    def open_google_maps(self, query):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            cleaned_dest = query.lower().replace("open google maps", "").replace("go to", "").replace("directions to", "").strip()
            gmm_intent_uri = Uri.parse(f"geo:0,0?q={urllib.parse.quote(cleaned_dest)}")
            map_intent = Intent(Intent.ACTION_VIEW, gmm_intent_uri)
            map_intent.setPackage("com.google.android.apps.maps")
            
            PythonActivity.mActivity.startActivity(map_intent)
        except Exception:
            self.output_label.text = "Zeta: Environment restriction detected. Operating system native components require an active Android compilation profile."

    def open_target_app(self, query):
        # Programmatic Android Package Name App Switching Matrix
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            current_activity = PythonActivity.mActivity
            pm = current_activity.getPackageManager()
            
            # Common App Selection Maps
            app_name = query.lower().replace("open app", "").replace("launch", "").strip()
            package_name = "com.android.settings" # Default Fallback Configuration Target
            
            if "youtube" in app_name: package_name = "com.google.android.youtube"
            elif "chrome" in app_name: package_name = "com.android.chrome"
            elif "whatsapp" in app_name: package_name = "com.whatsapp"
            elif "facebook" in app_name: package_name = "com.facebook.katana"
            
            launch_intent = pm.getLaunchIntentForPackage(package_name)
            if launch_intent:
                current_activity.startActivity(launch_intent)
            else:
                self.output_label.text = f"Zeta: Unable to locate package link matching '{app_name}' on this device grid."
        except Exception:
            self.output_label.text = "Zeta: Mainframe execution failed. App links are only operational inside native APK distributions."

    def generate_image_ai(self, text_prompt):
        cleaned_prompt = text_prompt.lower().replace("generate image", "").replace("draw", "").strip()
        url = "https://huggingface.co"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        try:
            req = urllib.request.Request(url, data=json.dumps({"inputs": cleaned_prompt}).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
                data_io = io.BytesIO(img_data)
                
                # Dynamic Texture Buffering to present graphics live on UI stack
                core_img = CoreImage(data_io, ext="png")
                self.clear_widgets()
                
                # Render Image Frame alongside a recovery button to return to terminal console view
                display_widget = Image(texture=core_img.texture)
                self.add_widget(display_widget)
                
                reset_btn = Button(text="Return to Main Console Interface", size_hint_y=0.1)
                reset_btn.bind(on_press=lambda x: self.__init__())
                self.add_widget(reset_btn)
        except Exception:
            self.output_label.text = "Zeta: Imaging arrays failed to resolve target graphics arrays. Hugging Face key structure may be invalid."

class ZetaApp(App):
    def build(self):
        return ZetaInterface()

if __name__ == '__main__':
    ZetaApp().run()
        
