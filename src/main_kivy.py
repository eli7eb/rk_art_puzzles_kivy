from functools import partial


import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder

from src.settings.kivy import KivySettings
from src.event.command.scene import SceneChangeCommand
from src.event.command.scene import SceneChangeController

from src.screen.game import GameScreen
from src.game_consts.game_constants import *
from src.screen.load_data import LoadDataScreen
from src.game_utils.game_logger import RkLogger
from src.kivy_game_widgets.kivy_tiles_grid import GameTilesGrid


play_level = None
class MainWindow(ScreenManager):


    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        # Create a consumer of SceneChangeCommands.
        self.scene_change_controller = SceneChangeController()

        # Periodically add an update call.
        Clock.schedule_interval(partial(self.update), 1/60.0)

        self.logger = RkLogger.__call__().get_logger()

    def change_scene(self, scene_name, *args):
        """Queues an attempt to change the scene.
        """
        known_screens = (
            'splash_creen',
            'title_screen',
            'load_data_screen',
            'menu_screen',
            'game_screen',
        )
        # If it's not a known scene, ignore it
        if not scene_name in known_screens:
            return

        # if load screen pass the mood
        if scene_name == "load_data_screen":
            play_level = levels[1]
        # Create a new SceneChangeCommand with the new scene.
        new_command = SceneChangeCommand(actor=self, scene=scene_name, args=args)

        # Add the new command to the contorller.
        self.scene_change_controller.add_command(new_command)

    def get_level(self):

        return levels[1]

    def update(self, dt):
        """Tries to execute periodically.
        dt = The amount of time.
        """
        # Process all scene change commands.
        self.scene_change_controller.process_commands()

class TitleScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def process_text(self):
        logger = RkLogger.__call__().get_logger()
        logger.info("mood_str " + self.ids.input.text)
        self.switch_to_load_data_screen()

    def switch_to_load_data_screen(self):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("load_data_screen")

    def switch_to_game_screen(self):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("game_screen",None)


class MainKivyRKrApp(App):
    def build(self):
        screen_manager = MainWindow(transition=FadeTransition())
        screen_manager.add_widget(TitleScreen(name="title_screen"))
        screen_manager.add_widget(GameScreen(name="game_screen"))
        screen_manager.add_widget(LoadDataScreen(name="load_data_screen"))
        screen_manager.current = 'title_screen'
        return screen_manager

kv = Builder.load_file("kv_data/game_kv.kv")
if __name__ == '__main__':
    # First set up graphics settings.
    # Config.set('graphics', 'width', '200')
    # Config.set('graphics', 'height', '800')

    # 0 being off 1 being on as in true / false
    # you can use 0 or 1 && True or False
    Config.set('graphics', 'resizable', '0')

    # fix the width of the window
    Config.set('graphics', 'width', '600')

    # fix the height of the window
    Config.set('graphics', 'height', '800')

    MainKivyRKrApp().run()

