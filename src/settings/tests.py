import os

from unittest import TestCase
from unittest.mock import MagicMock

from settings.kivy import KivySettings

class KivySettingsTest(TestCase):
    def setUp(self):
        """Make a temporary file during testing.
        """
        self.config_filename = 'test.txt'

    def tearDown(self):
        """Delete the temporary file.
        """
        try:
            os.remove(self.config_filename)
        except OSError as e:
            # The file most likely doesn't exist. That's okay.
            pass

    def test_default_settings(self):
        """Create activity settings config. Do not apply settings.
        Make sure defaults are set.
        """
        settings = KivySettings(apply_settings=False, filename=self.config_filename)

        fullscreen = settings.get_setting('fullscreen')
        self.assertTrue(fullscreen)

    def test_load_settings(self):
        """Create graphics settings object. Passing a filename object.
        Make sure the settings are read from this device.
        """

        try:
            new_config_filename = 'test2.txt'
            with open(new_config_filename, 'w') as config_file:
                config_file.writelines([
                    "[graphics]\n",
                    "fullscreen = 0\n",
                ])
            settings = KivySettings(apply_settings=False, filename=new_config_filename)

            fullscreen = settings.get_setting('fullscreen')
            self.assertEqual('0', fullscreen)
        finally:
            # delete the file
            try:
                os.remove(new_config_filename)
            except OSError as e:
                # The file most likely doesn't exist. That's okay.
                pass

    def test_change_settings(self):
        """Create a graphing setting object.
        Change one of the settings
        make sure the setting has been changed.
        """
        settings = KivySettings(apply_settings=False, filename=self.config_filename)

        original_fullscreen = settings.get_setting('fullscreen')
        if original_fullscreen == 'auto':
            settings.change_settings('fullscreen', '0')
        else:
            settings.change_settings('fullscreen', 'auto')
        new_fullscreen = settings.get_setting('fullscreen')
        self.assertNotEqual(original_fullscreen, new_fullscreen)

    def test_save_settings(self):
        """Create a graphic settings object.
        Change one of the settings and save.
        Make sure the settings file has new settings.
        """

        settings = KivySettings(apply_settings=False, filename=self.config_filename)

        original_fullscreen = settings.get_setting('fullscreen')
        if original_fullscreen == 'auto':
            settings.change_settings('fullscreen', '0')
        else:
            settings.change_settings('fullscreen', 'auto')

        new_fullscreen = settings.get_setting('fullscreen')

        # Write to the file
        settings.save_settings()

        # Read the file
        found_line = False
        with open(self.config_filename, 'r') as config_file:
            for line in config_file:
                if "fullscreen = auto" in line:
                    found_line = True
                    break
        self.assertTrue(found_line)
