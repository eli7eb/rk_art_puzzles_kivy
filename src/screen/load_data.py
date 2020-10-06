from functools import partial
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

from src.game_utils.game_logger import RkLogger


class LoadDataScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.logger = RkLogger.__call__().get_logger()
        Clock.schedule_interval(
            partial(
                LoadDataScreen.update,
                self
            ),
            1.0 / 30.0
        )

    def switch_to_title_screen(self):
        """Close this widget and open the Title Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("title_screen",None)


    def update(self, dt):
        # Stop if this window isn't active.
        if not self.parent:
            return
        # get mood if not there - get a random one
        try:
            _mood_str = text = self.manager.screens[0].ids.input.text
        except:
            self.logger.error("no mood str")
        self.load_data(dt)

    def load_data(self, dt):
        pass