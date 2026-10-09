from kivy.app import App
from kivy.uix.label import Label


class FileManagerApp(App):
    def build(self):
        return Label(text="Android File Manager")


if __name__ == "__main__":
    FileManagerApp().run()
