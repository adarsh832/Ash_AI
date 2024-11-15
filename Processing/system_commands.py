from commands.volume_commands import VolumeCommands
from commands.app_commands import AppCommands
from commands.brightness_commands import BrightnessCommands
from commands.power_commands import PowerCommands
from commands.system_commands import SystemCommands
from commands.network_commands import NetworkCommands
from commands.media_commands import MediaCommands
from commands.file_commands import FileCommands
from commands.display_commands import DisplayCommands
from commands.input_commands import InputCommands
from commands.security_commands import SecurityCommands
from commands.accessibility_commands import AccessibilityCommands

class SystemCommandExecutor:
    def __init__(self):
        self.command_handlers = {
            'volume': VolumeCommands.execute,
            'brightness': BrightnessCommands.execute,
            'power': PowerCommands.execute,
            'app': AppCommands.execute,
            'system': SystemCommands.execute,
            'network': NetworkCommands.execute,
            'media': MediaCommands.execute,
            'file': FileCommands.execute,
            'display': DisplayCommands.execute,
            'input': InputCommands.execute,
            'security': SecurityCommands.execute,
            'accessibility': AccessibilityCommands.execute
        }

    def execute_command(self, category, command):
        """Execute the system command based on category and command"""
        if category in self.command_handlers:
            return self.command_handlers[category](command)
        return f"Unknown category: {category}" 