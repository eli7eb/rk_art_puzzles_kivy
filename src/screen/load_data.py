from functools import partial
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

from src.game_utils.game_load_data import LoadingData
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

    def next(self, dt):
        if self.ids.load_progress_bar.value >= 100:
            return False
        self.ids.load_progress_bar.value += 1

    def update(self, dt):
        # Stop if this window isn't active.
        if not self.parent:
            return
        # get mood if not there - get a random one
        try:
            mood_str = self.manager.screens[0].ids.input.text
        except:
            self.logger.error("no mood str")

        try:
            level = self.parent.get_level()
        except:
            self.logger.error("where is level")
        self.ids.load_progress_bar.value = 1
        Clock.schedule_interval(self.next, 1 / 25)
        try:
            self.load_data(mood_str,level)
        except:
            pass
        finally:
            Clock.schedule_interval(self.next, 1 / 25)
        self.switch_to_game_screen()


    def switch_to_game_screen(self):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("game_screen", None)

    def load_data(self, mood_str,level):
        self.ids.progress_label.text = "Searching image for " + mood_str
        ld = LoadingData(mood_str,level)
        self.ids.progress_label.text = "Loading image"
        ld.retrieve_image_data()
        image_data = ld.get_image()
        title, long_title = ld.get_image_info()
        self.ids.progress_label.text = "Get Ready to solve " + title

