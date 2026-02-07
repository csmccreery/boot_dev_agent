from pathlib import Path
from os.path import getsize
from .utils.path_manager import PathManager


def get_files_directory(working_directory, directory="."):
    manager = PathManager(working_directory, directory)

    path_error = manager.validate_dir()

    if not path_error:
        for file in manager.target_path.iterdir():
            size = getsize(file) 
            is_dir = file.is_dir()
            print(f"{file}: file_size={size}, is_dir={is_dir}")
    else:
        return path_error

        
            
    

    

    
