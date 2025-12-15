from os import makedirs
from os.path import (
        abspath,
        join,
        normpath,
        exists,
        dirname
        )

def write_file(working_directory, file_path, content):
    abs_working_path = abspath(working_directory) 
    full_path = normpath(join(
                abs_working_path, 
                file_path
                ))

    if not full_path.startswith(abspath(working_directory)):
        return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'

    if not exists(dirname(full_path)):
        makedirs(dirname(full_path))

    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

