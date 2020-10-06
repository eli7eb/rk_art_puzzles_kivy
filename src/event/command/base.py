class UnknownCommandException(Exception):
    pass

class Command(object):
    """Encapsulate an request that acts upon an object.
    """

    def __init__(self, *args, **kwargs):
        # Track the object that will act.
        self.actor = kwargs['actor']

        # Did the actor start executing?
        self.started_execution = False

        # Did the actor finish executing?
        self.finished_execution = False

    def has_started(self):
        """Returns True if the Command started execution.
        """
        return self.started_execution == True

    def has_finished(self):
        """Returns True if the Command finished execution.
        """
        return self.finished_execution == True

    def execute(self):
        """Perform the command on the actor.
        """
        self.started_execution = True

    def is_undoable(self):
        """Returns True if this Command's effects can be reverted.

        The base Command returns False;
        """
        return False

    def undo(self):
        """Reverse the effects of the execute command.
        """
        # The base command does nothing, so that's easy to undo.
        pass

class CommandController(object):
    """Base class that accepts a bunch of Command objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        # A list of Command objects
        self.command_queue = []

        # The most recently run commands that can be undone.
        self.undo_command_history = []

    def add_command(self, new_command):
        """Adds a Command to the queue.
        """
        self.command_queue.append(new_command)

    def process_commands(self):
        """Tries to process commands.
        """
        # If there are no commands, we're done.
        if len(self.command_queue) == 0:
            return

        # If the current command has started but not finished, wait for it to finish.
        current_command = None
        if len(self.command_queue) > 0:
            current_command = self.command_queue[0]
        if current_command and current_command.has_started() and not current_command.has_finished():
            return

        # Collect a list to remove after execution.
        commands_to_delete = []

        # For each command in the queue,
        for command in self.command_queue:
            # Get the command and try to execute it unless it is already running.
            if not command.has_started():
                self.handle_command(command)
                # If it did not start, then it means we don't recognize this command. Raise an Exception.
                if not command.has_started():
                    raise UnknownCommandException("Base CommandController cannot handle commands of type {command_type}.".format(command_type=type(current_command)))

            # If it finished, we need to manage the Undo stack.
            if command.has_finished():
                # If the command can be undone, add it to the undo stack.
                if command.is_undoable():
                    self.undo_command_history.append(command)
                else:
                    # Otherwise this is a permanent action. Clear the undo buffer.
                    self.undo_command_history.clear()

                # mark the command for removal.
                commands_to_delete.append(command)
        # Remove all commands in the queue.
        for command in commands_to_delete:
            self.command_queue.remove(command)

    def handle_command(self, command):
        """Subclasses will inspect and handle commands.
        They should mark the command has started execution.
        """
        pass

    def can_undo_last_command(self):
        """Returns True if the previously executed command can be reverted.
        """
        # If there is no previous command, nothing can be undone.
        if len(self.undo_command_history) == 0:
            return False
        return True

    def undo_last_command(self):
        """Revert the effects of the previously executed command.
        """
        # Make sure you can undo the last command.
        if not self.can_undo_last_command():
            return

        # Make sure you are not in mid execution.
        current_command = None
        if len(self.command_queue) > 0:
            current_command = self.command_queue[0]
        if current_command and current_command.has_started() and not current_command.has_finished():
            return

        # Undo the last command.
        undo_this_command = self.undo_command_history[-1]
        undo_this_command.undo()

        # Now that you've undone the last command, remove it.
        self.undo_command_history.remove(undo_this_command)
