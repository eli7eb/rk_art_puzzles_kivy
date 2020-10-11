from src.event.command.base import Command
from src.event.command.base import CommandController

class SceneChangeCommand(Command):
    """Change the current scene to the given ID.
    This operation is not reversible.
    """

    def __init__(self, *args, **kwargs):
        """actor: SceneManager
        scene: Desired scene to transition to.
        """
        super().__init__(self, *args, **kwargs)

        self.next_scene = kwargs['scene']

    def execute(self):
        """Transition to the next scene.
        """
        # Mark that you started execution
        self.started_execution = True

        # Execute the scene transition
        self.actor.current = self.next_scene

        # Mark that you finished execution
        self.finished_execution = True

    def is_undoable(self):
        return False

    def undo(self):
        return

class SceneChangeController(CommandController):
    """Manages scene transitions.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(self, *args, **kwargs)

    def handle_command(self, command):
        """Handle SceneChangeCommand
        """
        if isinstance(command, SceneChangeCommand):
            # Tell the command to act.
            command.execute()

