import subprocess

class MediaCommands:
    @staticmethod
    def execute(command):
        """Handle media-related commands"""
        actions = {
            'play': MediaCommands._play,
            'pause': MediaCommands._pause,
            'stop': MediaCommands._stop,
            'next': MediaCommands._next,
            'previous': MediaCommands._previous,
            'fast forward': MediaCommands._fast_forward,
            'rewind': MediaCommands._rewind,
            'shuffle': MediaCommands._shuffle,
            'repeat': MediaCommands._repeat,
            'mute audio': MediaCommands._mute_audio,
            'unmute audio': MediaCommands._unmute_audio
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing media command: {str(e)}"
        return f"Unrecognized media command: {command}"

    @staticmethod
    def _play():
        return "Playing media..."

    @staticmethod
    def _pause():
        return "Pausing media..."

    @staticmethod
    def _stop():
        return "Stopping media..."

    @staticmethod
    def _next():
        return "Playing next track..."

    @staticmethod
    def _previous():
        return "Playing previous track..."

    @staticmethod
    def _fast_forward():
        return "Fast forwarding..."

    @staticmethod
    def _rewind():
        return "Rewinding..."

    @staticmethod
    def _shuffle():
        return "Shuffling playlist..."

    @staticmethod
    def _repeat():
        return "Toggling repeat mode..."

    @staticmethod
    def _mute_audio():
        return "Muting audio..."

    @staticmethod
    def _unmute_audio():
        return "Unmuting audio..."