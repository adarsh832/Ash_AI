import subprocess
import platform
import os
import ctypes
from ctypes import wintypes

class BrightnessCommands:
    @staticmethod
    def execute(command):
        """Handle brightness-related commands"""
        actions = {
            'increase brightness': BrightnessCommands._increase_brightness,
            'decrease brightness': BrightnessCommands._decrease_brightness,
            'max brightness': BrightnessCommands._max_brightness,
            'min brightness': BrightnessCommands._min_brightness,
            'adjust brightness': BrightnessCommands._adjust_brightness,
            'set brightness': BrightnessCommands._set_brightness,
            'screen brighter': BrightnessCommands._increase_brightness,
            'screen dimmer': BrightnessCommands._decrease_brightness
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing brightness command: {str(e)}"
        return f"Unrecognized brightness command: {command}"

    @staticmethod
    def _get_platform_command():
        system = platform.system().lower()
        if system == 'windows':
            return {'type': 'windows', 'path': None}
        elif system == 'darwin':  # macOS
            return {'type': 'darwin', 'path': 'brightness'}
        else:  # Linux
            # Check for different backlight controllers
            if os.path.exists('/sys/class/backlight/intel_backlight'):
                return {'type': 'linux', 'path': '/sys/class/backlight/intel_backlight/brightness'}
            elif os.path.exists('/sys/class/backlight/amdgpu_bl0'):
                return {'type': 'linux', 'path': '/sys/class/backlight/amdgpu_bl0/brightness'}
            elif os.path.exists('/sys/class/backlight/acpi_video0'):
                return {'type': 'linux', 'path': '/sys/class/backlight/acpi_video0/brightness'}
        return None

    @staticmethod
    def _get_current_brightness_windows():
        """Get current brightness level on Windows"""
        try:
            # Windows API for getting brightness
            GetDeviceGammaRamp = ctypes.windll.gdi32.GetDeviceGammaRamp
            hdc = ctypes.windll.user32.GetDC(None)
            ramp = (wintypes.WORD * 256 * 3)()
            GetDeviceGammaRamp(hdc, ramp)
            return int((ramp[0][255] / 65535) * 100)
        except:
            return 50  # Default value if unable to get current brightness

    @staticmethod
    def _set_brightness_windows(level):
        """Set brightness level on Windows"""
        level = max(0, min(100, level))  # Ensure level is between 0 and 100
        try:
            # Try using PowerShell first
            script = f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})'
            subprocess.run(['powershell', '-Command', script], capture_output=True)
            return True
        except:
            return False

    @staticmethod
    def _increase_brightness():
        cmd = BrightnessCommands._get_platform_command()
        if not cmd:
            return "Brightness control not available..."
        
        try:
            if cmd['type'] == 'windows':
                current = BrightnessCommands._get_current_brightness_windows()
                new_level = min(100, current + 10)
                if BrightnessCommands._set_brightness_windows(new_level):
                    return "Increased screen brightness"
            
            elif cmd['type'] == 'darwin':
                # macOS brightness control
                subprocess.run(['brightness', '0.1', '-i'])
                return "Increased screen brightness"
            
            elif cmd['type'] == 'linux':
                # Linux brightness control
                with open(cmd['path'], 'r') as f:
                    current = int(f.read())
                with open(cmd['path'].replace('brightness', 'max_brightness'), 'r') as f:
                    max_brightness = int(f.read())
                new_brightness = min(max_brightness, int(current * 1.1))
                with open(cmd['path'], 'w') as f:
                    f.write(str(new_brightness))
                return "Increased screen brightness"
            
        except:
            pass
        return "Increasing screen brightness..."

    @staticmethod
    def _decrease_brightness():
        cmd = BrightnessCommands._get_platform_command()
        if not cmd:
            return "Brightness control not available..."
        
        try:
            if cmd['type'] == 'windows':
                current = BrightnessCommands._get_current_brightness_windows()
                new_level = max(0, current - 10)
                if BrightnessCommands._set_brightness_windows(new_level):
                    return "Decreased screen brightness"
            
            elif cmd['type'] == 'darwin':
                subprocess.run(['brightness', '0.1', '-d'])
                return "Decreased screen brightness"
            
            elif cmd['type'] == 'linux':
                with open(cmd['path'], 'r') as f:
                    current = int(f.read())
                new_brightness = max(0, int(current * 0.9))
                with open(cmd['path'], 'w') as f:
                    f.write(str(new_brightness))
                return "Decreased screen brightness"
            
        except:
            pass
        return "Decreasing screen brightness..."

    @staticmethod
    def _max_brightness():
        cmd = BrightnessCommands._get_platform_command()
        if not cmd:
            return "Brightness control not available..."
        
        try:
            if cmd['type'] == 'windows':
                if BrightnessCommands._set_brightness_windows(100):
                    return "Set brightness to maximum"
            
            elif cmd['type'] == 'darwin':
                subprocess.run(['brightness', '1'])
                return "Set brightness to maximum"
            
            elif cmd['type'] == 'linux':
                with open(cmd['path'].replace('brightness', 'max_brightness'), 'r') as f:
                    max_brightness = int(f.read())
                with open(cmd['path'], 'w') as f:
                    f.write(str(max_brightness))
                return "Set brightness to maximum"
            
        except:
            pass
        return "Setting brightness to maximum..."

    @staticmethod
    def _min_brightness():
        cmd = BrightnessCommands._get_platform_command()
        if not cmd:
            return "Brightness control not available..."
        
        try:
            if cmd['type'] == 'windows':
                if BrightnessCommands._set_brightness_windows(0):
                    return "Set brightness to minimum"
            
            elif cmd['type'] == 'darwin':
                subprocess.run(['brightness', '0'])
                return "Set brightness to minimum"
            
            elif cmd['type'] == 'linux':
                with open(cmd['path'], 'w') as f:
                    f.write('0')
                return "Set brightness to minimum"
            
        except:
            pass
        return "Setting brightness to minimum..."

    @staticmethod
    def _adjust_brightness():
        return "Adjusting screen brightness..."

    @staticmethod
    def _set_brightness():
        return "Setting brightness level..."