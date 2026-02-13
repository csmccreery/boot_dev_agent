from google.genai import types
from .get_files_info import schema_get_files_info
from .get_file_content import schema_get_file_content
from .write_file import schema_write_file
from .run_python import schema_run_python

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ],
)
