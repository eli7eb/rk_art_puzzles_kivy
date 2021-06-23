from functools import partial

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

from src.game_utils.game_logger import RkLogger
from src.kivy_game_widgets.kivy_game_dashboard import GameDashboard
from src.kivy_game_widgets.kivy_tiles_drag_container import GameTilesDragConatiner
from src.kivy_game_widgets.kivy_tiles_grid import GameTilesGrid
from kivy.properties import ObjectProperty

logger = RkLogger.__call__().get_logger()

class OptionsScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_interval(
            partial(
                OptionsScreen.update,
                self
            ),
            1.0 / 30.0
        )

        logger.info("OptionsScreen ")


    def on_enter(self, *args):
        pass

    def switch_to_title_screen(self):
        """Close this widget and open the Title Screen.
        """

        # Ask the parent to switch to the Game game_screens
        self.parent.change_scene("title_screen")

    def update(self, *args):
        # Stop if this window isn't active.
        if not self.parent:
            return

        #self.draw_tiles(dt)

    def btn(self):
        logger.info("game_time:", self.game_time.text)
        self.game_time.text = ""

    def validate_game_time(self):
        logger.info("validate_game_time:", self.game_time.text)
        pass

    def save_options(self):
        logger.info("save_options:", self.game_time.text)
        pass