import random
from functools import partial
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import StringProperty

from src.event.rk_event_dispatcher import RkEventDispatcher
from src.kivy_game_widgets.kivy_game_load_data import LoadingGameData
from src.game_utils.game_logger import RkLogger
from src.game_consts.game_constants import MOOD_IDEAS

class LoadDataScreen(Screen):
    loading_label = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass

    def screen_on_enter(self):
        self.load_data()


    def load_data(self):
        mood_str = random.choice(MOOD_IDEAS) if not self.manager.screens[0].ids.input.text else self.manager.screens[0].ids.input.text
        level = self.parent.get_level()
        self.loading_label = "Search painting for " + mood_str
        ld_params = {'mood_str': mood_str, 'level': level}

        ld = LoadingGameData(ld_params)
        ld.bind(on_load_data_complete=self.rk_callback)
        ld.bind(on_load_status_update=self.rk_update_callback)
        ld.retrieve_image_data()

    def rk_callback(self, *args):
        logger = RkLogger.__call__().get_logger()
        logger.info("rk_callback ")
        self.parent.change_scene("game_screen", args)
        # TODO self.ev.cancel()

    def rk_update_callback(value, *args):
        logger = RkLogger.__call__().get_logger()
        logger.info("rk_update_callback ")
        try:
            title = args[1]
            value.loading_label = title
        except:
            logger.error("error getting title")


    def switch_to_title_screen(self):
        """Close this widget and open the Title Screen.
        """

        # Ask the parent to switch to the Game game_screens
        self.parent.change_scene("title_screen",None)

    def next(self, dt):
        if self.ids.load_progress_bar.value >= 100:
            return False
        self.ids.load_progress_bar.value += 1

    def update(self, dt):
        pass

    def on_load_data_callback(self, *args):
        RkLogger.__call__().get_logger().info('on_load_data_callback is called with {}'.format(args))
        self.switch_to_game_screen(args)

    def on_load_status_update_callback(self, *args):
        RkLogger.__call__().get_logger().info('on_load_status_update_callback {}'.format(args))
        self.loading_label = str(args[1])


    def switch_to_game_screen(self,ret_object):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game game_screens
        self.parent.change_scene("game_screen", ret_object)

