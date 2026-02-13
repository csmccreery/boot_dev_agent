from pathlib import Path
from os.path import getsize
from .utils.path_manager import PathManager
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    manager = PathManager(working_directory, directory)
    path_error = manager.validate_dir()

    if not path_error:
        for file in manager.target_path.iterdir():
            size = getsize(file) 
            is_dir = file.is_dir()
            print(f"{file}: file_size={size}, is_dir={is_dir}")
    else:
        return path_error

        
            
    

    

    
