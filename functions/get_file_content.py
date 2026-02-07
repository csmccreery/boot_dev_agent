from pathlib import Path
from .utils.path_manager import PathManager

def get_file_content(working_directory, file_path):
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_file()

    if not path_error:
        with open(manager.target_path, 'r') as f:
            content = f.read(10000)

            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content
    else:
        return path_error
                
            
