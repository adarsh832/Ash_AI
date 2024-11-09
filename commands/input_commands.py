import subprocess

class InputCommands:
    @staticmethod
    def execute(command):
        """Handle input device-related commands"""
        actions = {
            'enable keyboard': InputCommands._enable_keyboard,
            'disable keyboard': InputCommands._disable_keyboard,
            'enable touchpad': InputCommands._enable_touchpad,
            'disable touchpad': InputCommands._disable_touchpad,
            'enable mouse': InputCommands._enable_mouse,
            'disable mouse': InputCommands._disable_mouse,
            'keyboard layout': InputCommands._keyboard_layout,
            'input language': InputCommands._input_language
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing input command: {str(e)}"
        return f"Unrecognized input command: {command}"

    @staticmethod
    def _enable_keyboard():
        return "Enabling keyboard..."

    @staticmethod
    def _disable_keyboard():
        return "Disabling keyboard..."

    @staticmethod
    def _enable_touchpad():
        return "Enabling touchpad..."

    @staticmethod
    def _disable_touchpad():
        return "Disabling touchpad..."

    @staticmethod
    def _enable_mouse():
        return "Enabling mouse..."

    @staticmethod
    def _disable_mouse():
        return "Disabling mouse..."

    @staticmethod
    def _keyboard_layout():
        return "Changing keyboard layout..."

    @staticmethod
    def _input_language():
        return "Changing input language..." 