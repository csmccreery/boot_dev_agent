from pathlib import Path
from .utils.path_manager import PathManager
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of files into stdout. If the file is > 10000 lines than it truncates the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to read files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_file()

    if not path_error:
        print(f"Reading content of file {file_path} into STDIN")
        with open(manager.target_path, 'r') as f:
            content = f.read(10000)

            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content
    else:
        return path_error
                
            
