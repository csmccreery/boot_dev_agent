from .utils.path_manager import PathManager
from os import makedirs

def write_file(working_directory, file_path, content) -> None:
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_write()

    if not path_error:
        try:
            if not manager.target_path.exists():
                makedirs(manager.target_path.parent, exist_ok=True)

            with open(manager.target_path, 'w') as fp:
                fp.write(content)

            return f"Succesfully wrote to '{file_path}' ({len(content)} characters written)"
        except Exception as e:
            return f"Error: {e}"
    else:
        return path_error
