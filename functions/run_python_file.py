from os.path import (
        getsize,
        abspath,
        join,
        isfile,
        normpath
        )

def run_python_file(working_directory, file_path, args=[]):
    abs_working_path = abspath(working_directory)

    full_path = normpath(join(
                abs_working_path,
                file_path
                ))

    if not full_path.startswith(abs_working_path):
        return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'

    if not isfile(full_path):
        return f'Error: File "{full_path}" not found'

    if not full_path.endswith(".py"):
        return f'Error: File "{full_path}" not a python file'

