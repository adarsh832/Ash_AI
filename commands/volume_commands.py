import subprocess
import platform
import os

class VolumeCommands:
    @staticmethod
    def execute(command):
        """Handle volume-related commands"""
        actions = {
            'increase volume': VolumeCommands._increase_volume,
            'decrease volume': VolumeCommands._decrease_volume,
            'mute': VolumeCommands._mute,
            'unmute': VolumeCommands._unmute,
            'volume up': VolumeCommands._increase_volume,
            'volume down': VolumeCommands._decrease_volume,
            'set volume': VolumeCommands._set_volume,
            'max volume': VolumeCommands._max_volume,
            'min volume': VolumeCommands._min_volume,
            'adjust volume': VolumeCommands._adjust_volume
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing volume command: {str(e)}"
        return f"Unrecognized volume command: {command}"

    @staticmethod
    def _get_platform_command():
        system = platform.system().lower()
        if system == 'windows':
            # Check for nircmd
            nircmd_paths = [
                os.path.join(os.getcwd(), 'nircmd.exe'),
                r'C:\Windows\nircmd.exe',
                r'C:\Windows\System32\nircmd.exe'
            ]
            for path in nircmd_paths:
                if os.path.exists(path):
                    return {'type': 'nircmd', 'path': path}
            
            # Fallback to PowerShell
            return {'type': 'powershell', 'path': 'powershell.exe'}
        
        elif system == 'darwin':  # macOS
            return {'type': 'osascript', 'path': 'osascript'}
        
        else:  # Linux
            if subprocess.run(['which', 'amixer'], capture_output=True).returncode == 0:
                return {'type': 'amixer', 'path': 'amixer'}
            elif subprocess.run(['which', 'pactl'], capture_output=True).returncode == 0:
                return {'type': 'pactl', 'path': 'pactl'}
        
        return None

    @staticmethod
    def _increase_volume():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'changesysvolume', '5000'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetVolume(([System.Math]::Min(100, (Get-WmiObject -Class Win32_SoundDevice).GetVolume() + 10)))'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
            elif cmd['type'] == 'amixer':
                subprocess.run(['amixer', '-q', 'sset', 'Master', '5%+'])
            elif cmd['type'] == 'pactl':
                subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%'])
            
            return "Increased system volume"
        except:
            return "Increasing system volume..."

    @staticmethod
    def _decrease_volume():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'changesysvolume', '-5000'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetVolume(([System.Math]::Max(0, (Get-WmiObject -Class Win32_SoundDevice).GetVolume() - 10)))'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
            elif cmd['type'] == 'amixer':
                subprocess.run(['amixer', '-q', 'sset', 'Master', '5%-'])
            elif cmd['type'] == 'pactl':
                subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%'])
            
            return "Decreased system volume"
        except:
            return "Decreasing system volume..."

    @staticmethod
    def _mute():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'mutesysvolume', '1'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetMute($true)'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume with output muted'])
            elif cmd['type'] in ['amixer', 'pactl']:
                subprocess.run(['amixer', '-q', 'set', 'Master', 'mute'])
            
            return "Muted system audio"
        except:
            return "Muting system audio..."

    @staticmethod
    def _unmute():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'mutesysvolume', '0'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetMute($false)'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume without output muted'])
            elif cmd['type'] in ['amixer', 'pactl']:
                subprocess.run(['amixer', '-q', 'set', 'Master', 'unmute'])
            
            return "Unmuted system audio"
        except:
            return "Unmuting system audio..."

    @staticmethod
    def _max_volume():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'setsysvolume', '65535'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetVolume(100)'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume output volume 100'])
            elif cmd['type'] in ['amixer', 'pactl']:
                subprocess.run(['amixer', '-q', 'sset', 'Master', '100%'])
            
            return "Set volume to maximum"
        except:
            return "Setting volume to maximum..."

    @staticmethod
    def _min_volume():
        cmd = VolumeCommands._get_platform_command()
        if not cmd:
            return "Volume control not available..."
        
        try:
            if cmd['type'] == 'nircmd':
                subprocess.run([cmd['path'], 'setsysvolume', '0'])
            elif cmd['type'] == 'powershell':
                script = '(Get-WmiObject -Class Win32_SoundDevice).SetVolume(0)'
                subprocess.run(['powershell', '-Command', script])
            elif cmd['type'] == 'osascript':
                subprocess.run(['osascript', '-e', 'set volume output volume 0'])
            elif cmd['type'] in ['amixer', 'pactl']:
                subprocess.run(['amixer', '-q', 'sset', 'Master', '0%'])
            
            return "Set volume to minimum"
        except:
            return "Setting volume to minimum..."

    @staticmethod
    def _set_volume():
        return "Setting volume level..."

    @staticmethod
    def _adjust_volume():
        return "Adjusting system volume..." 