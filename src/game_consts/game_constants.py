from src.game_levels.game_level import Level


# all level parameters are a calculation of LEVEL
# log levels to write into the log file:
# all print statement will go there
# log has ID = level message and params
LOG_LEVEL = 1

TILE_ON_BOARD_TEST = 0
TILE_INVISIBLE = 1
TILE_IN_TILES_BANK = 2
TILE_IN_PLACE = 3
TILE_DRAGGED = 4
TILE_DROPPED = 5

LEVEL_NEWBIE = 1
LEVEL_BEGIN = 2
LEVEL_INTER = 3
LEVEL_MASTER = 5
LEVEL_CHAMPION = 6
LEVEL_NOVICE = 7

levels = { \
    LEVEL_NEWBIE: Level(LEVEL_NEWBIE, 'newbie', True,4,6,True,0,True,0),
    LEVEL_BEGIN: Level(LEVEL_BEGIN, 'begin', True,4,6,True,0,True,0),
    LEVEL_INTER: Level(LEVEL_INTER, 'inter', True,5,7,True,0,True,0),
    LEVEL_MASTER: Level(LEVEL_MASTER, 'master', True,6,8, True,0,True,0),
    LEVEL_CHAMPION: Level(LEVEL_CHAMPION, 'champion', True,6,8, True,0,True,0),
    LEVEL_NOVICE: Level(LEVEL_NOVICE, 'novice', True,7,9, True,0,True,0)
}

PORTRAIT = 'portrait'
LANDSCAPE = 'landscape'

MOOD_IDEAS = ['lion', 'glass', 'book', 'money', 'chair', 'garden', 'flower', 'tree', 'snow', 'carpet', 'wall', 'art', 'spring', 'summer', 'winter', 'cat', 'dog', 'farm', 'king', 'prince', 'happy', 'castle', 'bread', 'flower', 'war', 'library']
