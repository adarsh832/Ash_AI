import subprocess
import platform
import os
import ctypes

class PowerCommands:
    @staticmethod
    def execute(command):
        """Handle power-related commands"""
        actions = {
            'shutdown': PowerCommands._shutdown,
            'restart': PowerCommands._restart,
            'sleep': PowerCommands._sleep,
            'wake up': PowerCommands._wake_up,
            'hibernate': PowerCommands._hibernate,
            'power off': PowerCommands._shutdown,
            'turn off': PowerCommands._shutdown,
            'reboot': PowerCommands._restart,
            'log out': PowerCommands._log_out,
            'sign out': PowerCommands._log_out,
            'lock screen': PowerCommands._lock_screen,
            'unlock screen': PowerCommands._unlock_screen
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing power command: {str(e)}"
        return f"Unrecognized power command: {command}"

    @staticmethod
    def _get_platform():
        return platform.system().lower()

    @staticmethod
    def _shutdown():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to shut down'], check=True)
            else:  # Linux
                subprocess.run(['shutdown', '-h', 'now'], check=True)
            return "Initiating system shutdown..."
        except:
            return "Failed to initiate shutdown. Make sure you have the required permissions."

    @staticmethod
    def _restart():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['shutdown', '/r', '/t', '0'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to restart'], check=True)
            else:  # Linux
                subprocess.run(['shutdown', '-r', 'now'], check=True)
            return "Initiating system restart..."
        except:
            return "Failed to initiate restart. Make sure you have the required permissions."

    @staticmethod
    def _sleep():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powercfg', '/hibernate', 'off'], check=True)
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to sleep'], check=True)
            else:  # Linux
                subprocess.run(['systemctl', 'suspend'], check=True)
            return "Putting system to sleep..."
        except:
            return "Failed to put system to sleep. Make sure you have the required permissions."

    @staticmethod
    def _hibernate():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powercfg', '/hibernate', 'on'], check=True)
                subprocess.run(['shutdown', '/h'], check=True)
            elif system == 'darwin':  # macOS not supported
                return "Hibernation is not supported on macOS"
            else:  # Linux
                subprocess.run(['systemctl', 'hibernate'], check=True)
            return "Hibernating system..."
        except:
            return "Failed to hibernate system. Make sure you have the required permissions."

    @staticmethod
    def _log_out():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['shutdown', '/l'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to log out'], check=True)
            else:  # Linux
                subprocess.run(['gnome-session-quit', '--logout', '--no-prompt'], check=True)
            return "Logging out current user..."
        except:
            return "Failed to log out. Make sure you have the required permissions."

    @staticmethod
    def _lock_screen():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                ctypes.windll.user32.LockWorkStation()
            elif system == 'darwin':  # macOS
                subprocess.run(['pmset', 'displaysleepnow'], check=True)
            else:  # Linux
                subprocess.run(['loginctl', 'lock-session'], check=True)
            return "Locking screen..."
        except:
            return "Failed to lock screen. Make sure you have the required permissions."

    @staticmethod
    def _unlock_screen():
        return "Screen unlock requires user authentication..."

    @staticmethod
    def _wake_up():
        system = PowerCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powercfg', '/requestsoverride', 'PROCESS', 'PowerCommandWake', 'DISPLAY'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['caffeinate', '-u', '-t', '1'], check=True)
            else:  # Linux
                subprocess.run(['xset', 'dpms', 'force', 'on'], check=True)
            return "Waking up system..."
        except:
            return "Failed to wake up system. Make sure you have the required permissions."