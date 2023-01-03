from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import time
from filesharer import FileSharer
import webbrowser

Builder.load_file('front-end.kv')


class CameraScreen(Screen):
    def start(self):
        # Starts camera and change Button text
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera.opacity = 1

    def stop(self):
        # Stops camera and change Button text
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        # Capture the image, saves it, and loads it on the screen
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f"files/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a link first"

    def create_link(self):
        """" Accessed the photo's filepath, uploaded it to the web, and then
         displayed the link in the label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        fileshare = FileSharer(file_path)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        # Copy link in the Clipboard, available for pasting
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        # Open the link with the default browser
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
