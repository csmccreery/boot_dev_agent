from .utils.path_manager import PathManager
import subprocess
def run_python_file(working_directory, file_path, *args):
    manager = PathManager(working_directory, file_path)

    path_error = manager.validate_py()

    if not path_error:
        try:
            command = ["python", manager.target_path]
            command.extend(args)

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
            
