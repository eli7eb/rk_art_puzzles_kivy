from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder

Builder.load_file("rk_puzzle.kv")

class MainWidget(RelativeLayout):
    pass

class RKGameApp(App):
    pass

RKGameApp().run()