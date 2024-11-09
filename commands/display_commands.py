import subprocess
import platform
import os
import ctypes
import winreg

class DisplayCommands:
    @staticmethod
    def execute(command):
        """Handle display-related commands"""
        actions = {
            'change resolution': DisplayCommands._change_resolution,
            'rotate screen': DisplayCommands._rotate_screen,
            'mirror display': DisplayCommands._mirror_display,
            'extend display': DisplayCommands._extend_display,
            'night mode': DisplayCommands._night_mode,
            'dark mode': DisplayCommands._dark_mode,
            'light mode': DisplayCommands._light_mode,
            'change wallpaper': DisplayCommands._change_wallpaper,
            'screen saver': DisplayCommands._screen_saver
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing display command: {str(e)}"
        return f"Unrecognized display command: {command}"

    @staticmethod
    def _get_platform():
        return platform.system().lower()

    @staticmethod
    def _change_resolution():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # List available resolutions
                result = subprocess.run(['wmic', 'desktopmonitor', 'get', 'ScreenHeight,ScreenWidth'], 
                                     capture_output=True, text=True)
                return f"Available resolutions:\n{result.stdout}\nUse 'set resolution [width] [height]' to change"
            elif system == 'darwin':  # macOS
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                     capture_output=True, text=True)
                return f"Display information:\n{result.stdout}"
            else:  # Linux
                result = subprocess.run(['xrandr'], capture_output=True, text=True)
                return f"Available resolutions:\n{result.stdout}"
        except:
            return "Failed to get display information"

    @staticmethod
    def _rotate_screen():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Rotate screen 90 degrees
                subprocess.run(['displayswitch', '/rotate:90'])
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell application "System Preferences" to reveal anchor "displaysDisplayTab" of pane "com.apple.preference.displays"'])
            else:  # Linux
                # Rotate primary display
                subprocess.run(['xrandr', '--output', 'primary', '--rotate', 'right'])
            return "Rotated screen"
        except:
            return "Failed to rotate screen"

    @staticmethod
    def _night_mode():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Enable/disable night light in Windows
                key_path = r"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.bluelightreductionstate\windows.data.bluelightreduction.bluelightreductionstate"
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, "Data", 0, winreg.REG_BINARY, b'\x02\x00\x00\x00')
                    winreg.CloseKey(key)
                    return "Toggled night mode"
                except:
                    return "Failed to toggle night mode"
            elif system == 'darwin':  # macOS
                subprocess.run(['nightlight', 'toggle'])
                return "Toggled night mode"
            else:  # Linux
                # Toggle night mode using redshift
                try:
                    subprocess.run(['redshift', '-O', '4500'])
                    return "Enabled night mode"
                except:
                    return "Please install redshift: sudo apt-get install redshift"
        except:
            return "Failed to toggle night mode"

    @staticmethod
    def _dark_mode():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Enable dark mode in Windows
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                    return "Enabled dark mode"
                except:
                    return "Failed to enable dark mode"
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to tell appearance preferences to set dark mode to true'])
                return "Enabled dark mode"
            else:  # Linux
                # This depends on the desktop environment
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', 'Adwaita-dark'])
                return "Enabled dark mode"
        except:
            return "Failed to enable dark mode"

    @staticmethod
    def _light_mode():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Enable light mode in Windows
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(key)
                    return "Enabled light mode"
                except:
                    return "Failed to enable light mode"
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell app "System Events" to tell appearance preferences to set dark mode to false'])
                return "Enabled light mode"
            else:  # Linux
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', 'Adwaita'])
                return "Enabled light mode"
        except:
            return "Failed to enable light mode"

    @staticmethod
    def _change_wallpaper():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Show wallpaper settings
                subprocess.run(['start', 'ms-settings:personalization-background'], shell=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell application "System Preferences" to reveal anchor "DesktopScreensaver" of pane "com.apple.preference.desktopscreensaver"'])
            else:  # Linux
                subprocess.run(['gnome-control-center', 'background'])
            return "Opening wallpaper settings..."
        except:
            return "Failed to open wallpaper settings"

    @staticmethod
    def _screen_saver():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                # Activate screen saver
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF140, 0)
            elif system == 'darwin':  # macOS
                subprocess.run(['open', '-a', 'ScreenSaverEngine'])
            else:  # Linux
                subprocess.run(['gnome-screensaver-command', '-a'])
            return "Activated screen saver"
        except:
            return "Failed to activate screen saver"

    @staticmethod
    def _mirror_display():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['displayswitch', '/clone'])
            elif system == 'darwin':  # macOS
                subprocess.run(['displayplacer', 'mirror'])
            else:  # Linux
                subprocess.run(['xrandr', '--output', 'HDMI-1', '--same-as', 'eDP-1'])
            return "Mirrored displays"
        except:
            return "Failed to mirror displays"

    @staticmethod
    def _extend_display():
        system = DisplayCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['displayswitch', '/extend'])
            elif system == 'darwin':  # macOS
                subprocess.run(['displayplacer', 'extend'])
            else:  # Linux
                subprocess.run(['xrandr', '--output', 'HDMI-1', '--auto', '--right-of', 'eDP-1'])
            return "Extended displays"
        except:
            return "Failed to extend displays" 