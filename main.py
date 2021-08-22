from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import pandas
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('frontend.kv')

class StartScreen(Screen):
    def edit(self):
        self.manager.current = "sheet_editor"
    def create_new(self):
        pass
    def browse(self):
        pass

class SheetEditor(Screen):
    def edit(self):
        pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()