from unittest import TestCase
from unittest.mock import MagicMock

from event.command.base import Command
from event.command.base import CommandController
from event.command.base import UnknownCommandException

class StringActor(object):
    """The object the Commands should act upon.
    """
    def __init__(self, *args, **kwargs):
        # The buffer that will be affected.
        self.buffer = ""

    def append_string(self, string):
        self.buffer = self.buffer + string

    def remove_string(self, string):
        # Find the string in the buffer starting from the right side.
        buffer_index = self.buffer.rfind(string)
        # If it's not found, abort
        if buffer_index == -1:
            return
        # Concatenate the part before the index and the part after the string.
        string_before = self.buffer[:buffer_index]
        string_after = self.buffer[buffer_index + len(string):]
        self.buffer = string_before + string_after

class AddToStringCommand(Command):
    """This command carries a pay load to add to the string.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        # The buffer that will be affected.
        self.payload = kwargs['payload']

        # based on the Payload, declare if this can be undone or not. Defaults to True.
        self.can_undo = kwargs.get('can_undo', True)

    def execute(self):
        """Add the payload to the buffer.
        """
        # Mark that you started execution
        self.started_execution = True

        # Execute
        self.actor.append_string(self.payload)

        # Mark that you finished execution
        self.finished_execution = True

    def is_undoable(self):
        """Returns True if this Command's effects can be reverted.
        """
        return self.can_undo

    def undo(self):
        """Reverse the effects of the execute command.
        """
        # Mark that you started execution
        self.started_execution = True

        # Execute
        self.actor.remove_string(self.payload)

        # Mark that you finished execution
        self.finished_execution = True

class BogusCommand(Command):
    """This is an unknown command type.
    """
    pass

class StringCommandController(CommandController):
    """This class manages a string that can be modified by commands.
    """
    def handle_command(self, command):
        """Handle AddToString commands.
        """
        if isinstance(command, AddToStringCommand):
            # Tell the command to act.
            command.execute()

class CommandTest(TestCase):
    """Affirms you can make Command objects.
    """
    def setUp(self):
        # Start a controller that can accept AddToStringCommand objects.
        self.controller = StringCommandController()

    def test_add_command(self):
        """ Add a Command to the Controller.
        """
        # Create an empty string buffer.
        string_buffer = StringActor()

        # Create a new AddToStringCommand.
        new_command = AddToStringCommand(actor=string_buffer, payload="A1")

        # Add the command to the controller.
        controller = StringCommandController()
        controller.add_command(new_command)

        # Make sure the command has not started and is not finished.
        self.assertFalse(new_command.has_started())
        self.assertFalse(new_command.has_finished())

        # Activate the controller so it can process commands.
        controller.process_commands()

        # The command finishes quickly, so make sure it is finished.
        self.assertTrue(new_command.has_started())
        self.assertTrue(new_command.has_finished())

        # Make sure the controller no longer has the command queued.
        self.assertEqual(len(controller.command_queue), 0)

        # Check the controller's buffer, it should have the contents of the string.
        self.assertEqual(string_buffer.buffer, "A1")

    def test_execute_multiple_commands(self):
        """After adding a command, execute it and make sure you can see its effects.
        """
        # Create an empty string buffer.
        string_buffer = StringActor()

        # Create a new AddToStringCommand.
        command1 = AddToStringCommand(actor=string_buffer, payload="A1")
        command2 = AddToStringCommand(actor=string_buffer, payload="B2")

        # Add the command to the controller.
        controller = StringCommandController()
        controller.add_command(command1)
        controller.add_command(command2)

        # Activate the controller so it can process commands.
        controller.process_commands()

        # Check the controller's buffer, it should have the contents of the string.
        self.assertEqual(string_buffer.buffer, "A1B2")

    def test_unknown_command(self):
        """ Process an Unknown Command to raise an Exception.
        """
        # Create an empty string buffer.
        string_buffer = StringActor()

        # Create a BogusCommand that won't be recognized.
        new_command = BogusCommand(actor=string_buffer)

        # Add the command to the controller.
        controller = StringCommandController()
        controller.add_command(new_command)

        # Activate the controller so it can process commands. It should raise an exception.
        with self.assertRaises(UnknownCommandException):
            controller.process_commands()

    def test_undo_command(self):
        """ Some Commands can be undone.
        """
        # Create an empty string buffer.
        string_buffer = StringActor()

        # Create new AddToStringCommands. One of them cannot be undone.
        command1 = AddToStringCommand(actor=string_buffer, payload="A1", can_undo=False)
        command2 = AddToStringCommand(actor=string_buffer, payload="B2")

        # Add the command to the controller.
        controller = StringCommandController()
        controller.add_command(command1)
        controller.add_command(command2)

        # Activate the controller so it can process commands.
        controller.process_commands()

        # Check the controller's buffer, it should have the contents of the string.
        self.assertEqual(string_buffer.buffer, "A1B2")

        # Make sure you can undo the last command.
        self.assertTrue(controller.can_undo_last_command())

        # Undo the last command and make sure the buffer is fixed.
        controller.undo_last_command()
        self.assertEqual(string_buffer.buffer, "A1")

        # Can you undo the last command?
        self.assertFalse(controller.can_undo_last_command())

        # Try undoing anyway, nothing should happen
        controller.undo_last_command()
        self.assertEqual(string_buffer.buffer, "A1")

    def test_undo_multiple_commands(self):
        """Test that multiple commands can be undone.
        """
        # Create an empty string buffer.
        string_buffer = StringActor()

        # Create new AddToStringCommands. All can be undone.
        command1 = AddToStringCommand(actor=string_buffer, payload="A1")
        command2 = AddToStringCommand(actor=string_buffer, payload="B2")

        # Add the command to the controller.
        controller = StringCommandController()
        controller.add_command(command1)
        controller.add_command(command2)

        # Activate the controller so it can process commands.
        controller.process_commands()

        # Check the controller's buffer, it should have the contents of the string.
        self.assertEqual(string_buffer.buffer, "A1B2")

        # Make sure you can undo the last command.
        self.assertTrue(controller.can_undo_last_command())

        # Undo the last command and make sure the buffer is fixed.
        controller.undo_last_command()
        self.assertEqual(string_buffer.buffer, "A1")

        # Can you undo the last command? You should be able to.
        self.assertTrue(controller.can_undo_last_command())

        # Try undoing.
        controller.undo_last_command()
        self.assertEqual(string_buffer.buffer, "")

