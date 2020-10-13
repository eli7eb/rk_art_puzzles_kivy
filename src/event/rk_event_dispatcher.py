from kivy.event import EventDispatcher
from src.game_utils.game_logger import RkLogger

class RkEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_update')
        self.register_event_type('on_complete')
        self.logger = RkLogger.__call__().get_logger()
        super(RkEventDispatcher, self).__init__(**kwargs)

    def go_work(self, value):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        RkLogger.get_logger().info('go_work {}'.format(value))
        #self.dispatch('on_complete', value)
        RkLogger.get_logger().info('go_work end {}'.format(value))

    def on_update(self, *args):
        RkLogger.__call__().get_logger().info('on_update ')

    def on_complete(self, *args):
        RkLogger.__call__().get_logger().info('on_complete ')
