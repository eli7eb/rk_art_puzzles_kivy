import random
from functools import partial
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

from src.kivy_game_widgets.kivy_game_load_data import LoadingGameData
from src.game_utils.game_logger import RkLogger
from src.game_consts.game_constants import MOOD_IDEAS

class LoadDataScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.logger = RkLogger.__call__().get_logger()

    def on_enter(self):
        RkLogger.__call__().get_logger().info('on_enter')
        Clock.schedule_once(self.load_data)

    def build(self):
        pass

    def load_data(self, dt):
        mood_str = self.manager.screens[0].ids.input.text
        if (mood_str == ''):
            mood_str = random.choice(MOOD_IDEAS)
        level = self.parent.get_level()
        self.ids.progress_label.text = "Searching image for " + mood_str
        d = {mood_str: mood_str, level: level}
        ld = LoadingGameData(d)
        # ld = LoadingGameData(d)
        ld.bind(on_load_data_complete=self.on_load_data_callback)
        Clock.schedule_once(ld.trigger_custom_event, d, 3)
        self.ids.progress_label.text = "Loading image " + mood_str

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
        pass

    def on_load_data_callback(*args):
        RkLogger.__call__().get_logger().info('my on_custom_event is called with {}'.format(args))

    def switch_to_game_screen(self,ret_object):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("game_screen", ret_object)

    def on_load_data_complete(self, obj):
        RkLogger.get_logger().info("back from load data")
        self.switch_to_game_screen(obj)