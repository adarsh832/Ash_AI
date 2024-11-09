import subprocess
import psutil

class SystemCommands:
    @staticmethod
    def execute(command):
        """Handle system-related commands"""
        actions = {
            'update': SystemCommands._update,
            'install': SystemCommands._install,
            'uninstall': SystemCommands._uninstall,
            'check status': SystemCommands._check_status,
            'clean temp': SystemCommands._clean_temp,
            'clear cache': SystemCommands._clear_cache,
            'check memory': SystemCommands._check_memory,
            'check cpu': SystemCommands._check_cpu,
            'check storage': SystemCommands._check_storage,
            'system info': SystemCommands._system_info,
            'task manager': SystemCommands._task_manager
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing system command: {str(e)}"
        return f"Unrecognized system command: {command}"

    @staticmethod
    def _update():
        return "Checking for system updates..."

    @staticmethod
    def _install():
        return "Installing software..."

    @staticmethod
    def _uninstall():
        return "Uninstalling software..."

    @staticmethod
    def _check_status():
        return "Checking system status..."

    @staticmethod
    def _clean_temp():
        return "Cleaning temporary files..."

    @staticmethod
    def _clear_cache():
        return "Clearing system cache..."

    @staticmethod
    def _check_memory():
        return "Checking memory usage..."

    @staticmethod
    def _check_cpu():
        return "Checking CPU usage..."

    @staticmethod
    def _check_storage():
        return "Checking storage space..."

    @staticmethod
    def _system_info():
        return "Displaying system information..."

    @staticmethod
    def _task_manager():
        return "Opening task manager..." 