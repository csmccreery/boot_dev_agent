from pathlib import Path
from os import makedirs
from os.path import getsize

class PathManager:
    def __init__(self, working_dir, path):
        self.absolute_working_dir = Path(working_dir).absolute()
        self.target_path = (self.absolute_working_dir / path).resolve()
        self.common_path = self.get_common_path()

    def get_common_path(self):
        zipped_parts = zip(*(p.parts for p in [self.absolute_working_dir, self.target_path]))

        common_parts = []
        for part_tuple in zipped_parts:
            if len(set(part_tuple)) == 1:
                common_parts.append(part_tuple[0])
            else:
                break

        return Path(*common_parts)

    def validate_dir(self):
        if not self.target_path.is_dir():
            return f"Error: '{self.target_path}' is not a directory"

        if not self.target_path.exists():
            return f"Error: No such file or directory {self.target_path}"

        if not self.common_path == self.absolute_working_dir:
            return f"Error: Cannot list '{self.target_path}' as it is outside the permitted working directory"

        return None

    def validate_file(self):
        if self.target_path.is_dir():
            return f"Error: '{self.target_path}' is a directory"

        if not self.target_path.exists():
            return f"Error: No such file or directory {self.target_path}"

        if not self.common_path == self.absolute_working_dir:
            return f"Error: Cannot list '{self.target_path}' as it is outside the permitted working directory"

        return None

    def validate_write(self):
        if self.target_path.is_dir():
            return f"Error: '{self.target_path}' is a directory"

        if not self.common_path == self.absolute_working_dir:
            return f"Error: Cannot list '{self.target_path}' as it is outside the permitted working directory"

        return None
