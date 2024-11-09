import subprocess
import platform
import os
import ctypes

class AppCommands:
    # Common application paths and commands
    APP_PATHS = {
        'windows': {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'explorer': 'explorer.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
            'vscode': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'spotify': r'C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe',
            'discord': r'C:\Users\%USERNAME%\AppData\Local\Discord\app-1.0.9004\Discord.exe',
            'steam': r'C:\Program Files (x86)\Steam\steam.exe',
            'vlc': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
            'paint': 'mspaint.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'edge': 'msedge.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe'
        },
        'darwin': {  # macOS
            'chrome': 'Google Chrome',
            'firefox': 'Firefox',
            'safari': 'Safari',
            'calculator': 'Calculator',
            'terminal': 'Terminal',
            'finder': 'Finder',
            'spotify': 'Spotify',
            'vscode': 'Visual Studio Code'
        },
        'linux': {
            'chrome': 'google-chrome',
            'firefox': 'firefox',
            'calculator': 'gnome-calculator',
            'terminal': 'gnome-terminal',
            'spotify': 'spotify',
            'vscode': 'code'
        }
    }

    @staticmethod
    def execute(command):
        """Handle application-related commands"""
        # Special cases for window management
        if command in ['minimize all', 'minimize all windows']:
            return AppCommands._minimize_all_windows()
        elif command in ['minimize current', 'minimize current window']:
            return AppCommands._minimize_current_window()
        
        # Regular app commands
        parts = command.split()
        action = parts[0]
        app_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        
        actions = {
            'open': AppCommands._open_app,
            'close': AppCommands._close_app,
            'start': AppCommands._open_app,
            'stop': AppCommands._close_app,
            'launch': AppCommands._open_app,
            'quit': AppCommands._close_app,
            'minimize': AppCommands._minimize_app,
            'maximize': AppCommands._maximize_app,
            'restore': AppCommands._restore_app,
            'force quit': AppCommands._close_app,
            'switch to': AppCommands._switch_to_app,
            'focus on': AppCommands._focus_on_app,
            'run app': AppCommands._open_app,
            'kill app': AppCommands._close_app
        }
        
        action_func = actions.get(action)
        if action_func and app_name:
            try:
                return action_func(app_name)
            except Exception as e:
                return f"Error executing app command: {str(e)}"
        elif not app_name:
            return f"No application specified for '{action}' command"
        return f"Unrecognized app command: {command}"
    
    @staticmethod
    def _open_app(app_name):
        """Open an application based on the operating system"""
        app_name_lower = app_name.lower()
        system = platform.system().lower()
        
        try:
            # Get system-specific app paths
            app_paths = AppCommands.APP_PATHS.get(system, {})
            
            # Try to find the app in our predefined paths
            if app_name_lower in app_paths:
                app_path = app_paths[app_name_lower]
                
                if system == 'windows':
                    # Expand environment variables in path
                    app_path = os.path.expandvars(app_path)
                    if os.path.exists(app_path):
                        subprocess.Popen(app_path)
                    else:
                        # Fallback to simple command if path doesn't exist
                        subprocess.Popen(app_path.split('\\')[-1])
                    return f"Opening {app_name}..."
                    
                elif system == 'darwin':  # macOS
                    subprocess.run(['open', '-a', app_path])
                    return f"Opening {app_name}..."
                    
                else:  # Linux
                    subprocess.Popen(app_path)
                    return f"Opening {app_name}..."
            
            # If app not in predefined paths, try direct command
            if system == 'windows':
                try:
                    subprocess.Popen(app_name_lower)
                except:
                    # Try with .exe extension
                    subprocess.Popen(f"{app_name_lower}.exe")
            elif system == 'darwin':
                subprocess.run(['open', '-a', app_name])
            else:
                subprocess.Popen(app_name_lower)
            
            return f"Opening {app_name}..."
            
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    
    @staticmethod
    def _close_app(app_name):
        """Close an application"""
        try:
            if platform.system() == 'Windows':
                subprocess.run(['taskkill', '/IM', f'{app_name}.exe'], check=True)
            else:
                subprocess.run(['pkill', app_name], check=True)
            return f"Closed {app_name}"
        except:
            return f"Closing {app_name}..."
    
    @staticmethod
    def _minimize_app(app_name):
        """Minimize an application window"""
        return f"Minimizing {app_name}..."
    
    @staticmethod
    def _maximize_app(app_name):
        """Maximize an application window"""
        return f"Maximizing {app_name}..."
    
    @staticmethod
    def _restore_app(app_name):
        """Restore an application window"""
        return f"Restoring {app_name}..."
    
    @staticmethod
    def _switch_to_app(app_name):
        """Switch to an application"""
        return f"Switching to {app_name}..."
    
    @staticmethod
    def _focus_on_app(app_name):
        """Focus on an application"""
        return f"Focusing on {app_name}..."
    
    @staticmethod
    def _minimize_all_windows():
        """Minimize all windows"""
        system = platform.system().lower()
        try:
            if system == 'windows':
                # Windows key + M
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Windows key press
                ctypes.windll.user32.keybd_event(0x4D, 0, 0, 0)  # M key press
                ctypes.windll.user32.keybd_event(0x4D, 0, 2, 0)  # M key release
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Windows key release
                return "Minimized all windows"
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell application "System Events" to set miniaturized of every window of every process to true'])
                return "Minimized all windows"
            else:  # Linux
                subprocess.run(['wmctrl', '-k', 'on'])
                return "Minimized all windows"
        except:
            return "Failed to minimize all windows"

    @staticmethod
    def _minimize_current_window():
        """Minimize the current active window"""
        system = platform.system().lower()
        try:
            if system == 'windows':
                # Alt + Space, N
                ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)    # Alt press
                ctypes.windll.user32.keybd_event(0x20, 0, 0, 0)    # Space press
                ctypes.windll.user32.keybd_event(0x20, 0, 2, 0)    # Space release
                ctypes.windll.user32.keybd_event(0x4E, 0, 0, 0)    # N press
                ctypes.windll.user32.keybd_event(0x4E, 0, 2, 0)    # N release
                ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)    # Alt release
                return "Minimized current window"
            elif system == 'darwin':  # macOS
                subprocess.run(['osascript', '-e', 'tell application "System Events" to set miniaturized of window 1 of (first process whose frontmost is true) to true'])
                return "Minimized current window"
            else:  # Linux
                subprocess.run(['xdotool', 'windowminimize', '$(xdotool getactivewindow)'])
                return "Minimized current window"
        except:
            return "Failed to minimize current window"
    
    # Add other app-related methods... 