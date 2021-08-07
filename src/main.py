import kivy  # importing main package
from kivy.app import App  # required base class for your app.
from kivy.uix.label import Label  # uix element that will hold text
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

kivy.require("1.10.1")  # make sure people running py file have right version

# Our simple app. NameApp  convention matters here. Kivy
# uses some magic here, so make sure you leave the App bit in there!
# pos_hint = {“x”:1, “y”:1, “left”:1, “right”:1, “center_x”:1,
#                  “center_y”:1, “top”:1, “bottom”:1(“top”:0)}

class MainScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class OptionsScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

main_kv = Builder.load_file("main.kv")
class MainApp(App):
    # This is your "initialize" for the root wiget
    def build(self):
        # Creates that label which will just hold text.
        return main_kv


# Run the app.
if __name__ == "__main__":
    MainApp().run()