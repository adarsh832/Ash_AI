import subprocess
import platform
import os
import socket
import re

class NetworkCommands:
    @staticmethod
    def execute(command):
        """Handle network-related commands"""
        actions = {
            'wifi on': NetworkCommands._wifi_on,
            'wifi off': NetworkCommands._wifi_off,
            'connect wifi': NetworkCommands._connect_wifi,
            'disconnect wifi': NetworkCommands._disconnect_wifi,
            'bluetooth on': NetworkCommands._bluetooth_on,
            'bluetooth off': NetworkCommands._bluetooth_off,
            'airplane mode': NetworkCommands._toggle_airplane_mode,
            'check internet': NetworkCommands._check_internet,
            'network status': NetworkCommands._network_status,
            'show wifi networks': NetworkCommands._show_wifi_networks
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing network command: {str(e)}"
        return f"Unrecognized network command: {command}"

    @staticmethod
    def _get_platform():
        return platform.system().lower()

    @staticmethod
    def _wifi_on():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'enabled'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'], check=True)
            else:  # Linux
                subprocess.run(['nmcli', 'radio', 'wifi', 'on'], check=True)
            return "WiFi turned on"
        except:
            return "Failed to turn on WiFi. Make sure you have the required permissions."

    @staticmethod
    def _wifi_off():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'disabled'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportpower', 'en0', 'off'], check=True)
            else:  # Linux
                subprocess.run(['nmcli', 'radio', 'wifi', 'off'], check=True)
            return "WiFi turned off"
        except:
            return "Failed to turn off WiFi. Make sure you have the required permissions."

    @staticmethod
    def _connect_wifi():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                # Show available networks and let user select
                subprocess.run(['netsh', 'wlan', 'show', 'networks'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'], check=True)
                # Show available networks
                subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'], check=True)
            else:  # Linux
                subprocess.run(['nmcli', 'device', 'wifi', 'list'], check=True)
            return "Showing available WiFi networks. Please select a network to connect."
        except:
            return "Failed to show WiFi networks. Make sure WiFi is enabled."

    @staticmethod
    def _disconnect_wifi():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['netsh', 'wlan', 'disconnect'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportpower', 'en0', 'off'], check=True)
                subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'], check=True)
            else:  # Linux
                subprocess.run(['nmcli', 'device', 'disconnect', 'wifi'], check=True)
            return "Disconnected from WiFi"
        except:
            return "Failed to disconnect from WiFi."

    @staticmethod
    def _bluetooth_on():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powershell', '-Command', 'Set-BluetoothStatus -BluetoothStatus On'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['blueutil', '-p', '1'], check=True)
            else:  # Linux
                subprocess.run(['bluetoothctl', 'power', 'on'], check=True)
            return "Bluetooth turned on"
        except:
            return "Failed to turn on Bluetooth. Make sure you have the required permissions."

    @staticmethod
    def _bluetooth_off():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powershell', '-Command', 'Set-BluetoothStatus -BluetoothStatus Off'], check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['blueutil', '-p', '0'], check=True)
            else:  # Linux
                subprocess.run(['bluetoothctl', 'power', 'off'], check=True)
            return "Bluetooth turned off"
        except:
            return "Failed to turn off Bluetooth. Make sure you have the required permissions."

    @staticmethod
    def _check_internet():
        try:
            # Try to connect to Google's DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return "Internet connection is active"
        except OSError:
            return "No internet connection detected"

    @staticmethod
    def _network_status():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
                return f"Network Status:\n{result.stdout}"
            elif system == 'darwin':  # macOS
                result = subprocess.run(['networksetup', '-getinfo', 'Wi-Fi'], capture_output=True, text=True)
                return f"Network Status:\n{result.stdout}"
            else:  # Linux
                result = subprocess.run(['nmcli', 'device', 'status'], capture_output=True, text=True)
                return f"Network Status:\n{result.stdout}"
        except:
            return "Failed to get network status"

    @staticmethod
    def _show_wifi_networks():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)
                return f"Available WiFi Networks:\n{result.stdout}"
            elif system == 'darwin':  # macOS
                result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'], 
                                     capture_output=True, text=True)
                return f"Available WiFi Networks:\n{result.stdout}"
            else:  # Linux
                result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True)
                return f"Available WiFi Networks:\n{result.stdout}"
        except:
            return "Failed to show WiFi networks"

    @staticmethod
    def _toggle_airplane_mode():
        system = NetworkCommands._get_platform()
        try:
            if system == 'windows':
                subprocess.run(['powershell', '-Command', '(New-Object -ComObject Shell.Application).ToggleAirplaneMode()'], check=True)
            elif system == 'darwin':  # macOS
                # macOS doesn't have a direct command for airplane mode
                return "Airplane mode toggle not supported on macOS"
            else:  # Linux
                subprocess.run(['nmcli', 'radio', 'all', 'off'], check=True)  # Turn all radios off
            return "Toggled airplane mode"
        except:
            return "Failed to toggle airplane mode" 