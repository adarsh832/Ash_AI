import os
import shutil

class FileCommands:
    @staticmethod
    def execute(command):
        """Handle file-related commands"""
        actions = {
            'copy': FileCommands._copy,
            'paste': FileCommands._paste,
            'cut': FileCommands._cut,
            'delete': FileCommands._delete,
            'rename': FileCommands._rename,
            'move': FileCommands._move,
            'new folder': FileCommands._new_folder,
            'new file': FileCommands._new_file,
            'compress': FileCommands._compress,
            'extract': FileCommands._extract,
            'download': FileCommands._download,
            'upload': FileCommands._upload,
            'share': FileCommands._share,
            'search files': FileCommands._search_files
        }
        
        action = actions.get(command)
        if action:
            try:
                return action()
            except Exception as e:
                return f"Error executing file command: {str(e)}"
        return f"Unrecognized file command: {command}"

    @staticmethod
    def _copy():
        return "Copying file..."

    @staticmethod
    def _paste():
        return "Pasting file..."

    @staticmethod
    def _cut():
        return "Cutting file..."

    @staticmethod
    def _delete():
        return "Deleting file..."

    @staticmethod
    def _rename():
        return "Renaming file..."

    @staticmethod
    def _move():
        return "Moving file..."

    @staticmethod
    def _new_folder():
        return "Creating new folder..."

    @staticmethod
    def _new_file():
        return "Creating new file..."

    @staticmethod
    def _compress():
        return "Compressing file..."

    @staticmethod
    def _extract():
        return "Extracting archive..."

    @staticmethod
    def _download():
        return "Downloading file..."

    @staticmethod
    def _upload():
        return "Uploading file..."

    @staticmethod
    def _share():
        return "Sharing file..."

    @staticmethod
    def _search_files():
        return "Searching for files..." 