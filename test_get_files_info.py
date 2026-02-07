from functions.get_files_info import *

print(get_files_directory('calculator', '.'))
print(get_files_directory('calculator', 'pkg'))
print(get_files_directory('calculator', '/bin'))
print(get_files_directory('calculator', '../'))
