import kivy  # importing main package
from kivy.app import App  # required base class for your app.
from kivy.uix.label import Label  # uix element that will hold text
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

kivy.require("1.10.1")  # make sure people running py file have right version

# Our simple app. NameApp  convention matters here. Kivy
# uses some magic here, so make sure you leave the App bit in there!


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

from src.game_consts.game_constants import LEVEL_BEGIN

from pygame.locals import *
from src.game_views.load_resource_view import LoadingView
from src.game_views.text_view import TextView
from src.game_views.main_menu_view import MenuView
from src.game_views.quit_view import QuitView
from src.game_views.game_view import GameView
from src.game_consts.game_constants import *
from src.game_utils.game_logger import RkLogger
from src.game_consts.game_constants import *

# TODO make the players think before trying so reward on success at first attempt
# TODO and minus score on successive same tries
# TODO non equal tiles for next version



WIDTH, HEIGHT = 750, 750
level = levels[1]
# load resources
# constants
WIDTH, HEIGHT = 750, 750


HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2


