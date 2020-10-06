from kivy.config import Config

class KivySettings(object):
    """This class handles all of the Kivy-specific config settings.
    """

    def __init__(self, *args, **kwargs):
        self.load_settings(**kwargs)
        self.apply_settings()

    def load_settings(self, **kwargs):
        """Load graphics configuration settings. Does not actually apply settings.
        filename - optional string argument. This will try to open the file with that filename instead.

        If no argument is used, the function will use the built-in Kivy configuration (or default values if it can't be found.)
        """

        # Open the config file for reading.
        self.config_filename = kwargs.get('filename', None)

        if self.config_filename:
            Config.read(self.config_filename)

        # If a file wasn't used, use Kivy's Config object, or use a default if it isn't found.
        self.temporary_fullscreen = Config.getdefault('graphics', 'fullscreen', 'auto')

    def save_settings(self, **kwargs):
        """Saves the current graphics configuration settings, if a file was provided.
        """

        # For each setting name & value, set it
        value_by_name = self._get_setting_name_to_field()

        Config.set('graphics', 'fullscreen', self.__dict__[ value_by_name['fullscreen'] ])

        # Write the to config file, if given.
        if self.config_filename:
            Config.write()

    def apply_settings(self):
        """After loading the settings, this will actually apply the changes.
        This will affect settings.
        """
        #from kivy.core.window import Window
        #TODO: research to these graphics settings and then apply them here.
        pass

    def _get_setting_name_to_field(self):
        """Returns a dictionary assigning public-facing setting names to class field.
        """
        setting_name_to_field = {
            'fullscreen' : 'temporary_fullscreen',
        }

        # Make sure every field is actually present in the object.
        for field in setting_name_to_field.values():
            val = vars(self)[field]

        return setting_name_to_field

    def change_settings(self, setting_name, value):
        """Changes the giving setting name to the given value.
        """

        # Find out which field the setting will change.
        value_by_name = self._get_setting_name_to_field()
        field_name = value_by_name[setting_name]

        # Set that field.
        self.__dict__[field_name] = value

    def get_setting(self, setting_name):
        """Returns the value for the given setting.
        """
        # Find out which field the setting will change.
        value_by_name = self._get_setting_name_to_field()
        field_name = value_by_name[setting_name]

        # Get that field.
        return self.__dict__[field_name]
