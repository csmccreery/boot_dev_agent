from .utils.path_manager import PathManager
from google.genai import types
import subprocess


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python code within a given directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to find executable python files, relative to the working directory (default is the working directory itself)",
            ),
            "arguments": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A string argument that will be joined to form the arguments passed into a python program."
                ),
                description="A list of strings that serve as arguments to the python file to be run"
            ),
        },
        required=['file_path', 'arguments']
    ),
)


def run_python_file(working_directory, file_path, arguments):
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_py()

    if not path_error:
        try:
            command = ["python", manager.target_path]
            command.extend(arguments)

            res = subprocess.run(command, capture_output=True, text=True, timeout=30)

            return_code = res.returncode
            stdout = res.stdout
            stderr = res.stderr

            output_str = []
            if return_code != 0:
                output_str.append(f"Process exited with code {return_code}")

            if (not stderr and not stdout):
                output_str.append("No output produced")

            output_str.append(f"STDOUT: {stdout}")
            output_str.append(f"STDERR: {stderr}")
            return " ".join(output_str)
            
        except Exception as e:
            return f"Error: {e}"

    else:
        return path_error
            
