from functools import partial

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

from src.kivy_game_widgets.kivy_game_dashboard import GameDashboard
from src.kivy_game_widgets.kivy_tiles_drag_container import GameTilesDragConatiner
from src.kivy_game_widgets.kivy_tiles_grid import GameTilesGrid
from kivy.properties import ObjectProperty

grid_tiles = GameTilesGrid()
drag_tiles = GameTilesDragConatiner()
dashboard = GameDashboard()


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_interval(
            partial(
                GameScreen.update,
                self
            ),
            1.0 / 30.0
        )


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
        grid_tiles.draw_tiles()
        #self.draw_tiles(dt)



    def draw_tiles(self, dt):
        """
        """

        # Stop if this window isn't active.
        if not self.parent:
            return

        mapX = 100
        mapY = 200

        # Draw a box before drawing gui elements
        with self.canvas.before:
            for y in range(5):
                if y % 2 == 1:
                    offset = 25
                else:
                    offset = 0
                for x in range(5):
                    self.draw_tile(mapX + offset + x * 50, mapY + y * 50)

    def draw_tile(self, x, y):
        """Draw a tile at given the location.
        """
        Color(0.2, 0.2, 0.2)
        Rectangle(pos=(x,y), size=(50, 50))
        Color(1.0, 0.0, 0.0)
        Rectangle(pos=(x+1,y+1), size=(48, 48))
