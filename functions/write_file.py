from .utils.path_manager import PathManager
from os import makedirs
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file, overwriting any existing files and creating any parent directories as needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to write to files, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content that will be input into the file. This can be raw text, arbitrary code, or state secrets"
            ),
        },
    ),
)


def write_file(working_directory, file_path, content) -> None:
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_write()

    if not path_error:
        try:
            if not manager.target_path.exists():
                makedirs(manager.target_path.parent, exist_ok=True)

            with open(manager.target_path, 'w') as fp:
                fp.write(content)

            return f"Succesfully wrote {content} to '{file_path}' ({len(content)} characters written)"
        except Exception as e:
            return f"Error: {e}"
    else:
        return path_error
