from os import makedirs
from google.genai import types

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

schema = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, constrained within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the root of the project ('.')",
                ),

            "content" : types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
                )
        },
    ),
)


