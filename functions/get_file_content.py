from google.genai import types

from os.path import (
        getsize,
        abspath,
        join,
        isfile,
        normpath
        )

MAX_READ_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = normpath(join(
                abspath(working_directory), 
                file_path
                ))

    if not full_path.startswith(abspath(working_directory)):
        return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'

    if not isfile(full_path):
        return f'Error: File not found or is not a regular file: "{full_path}"'

    try:
        with open(full_path, "r") as f:
            content = f.read(MAX_READ_CHARS)

        if getsize(full_path) > MAX_READ_CHARS:

            return f"...{content}\n[File \"{full_path}\" truncated at 10000 characters]"
        else:
            return content
    except Exception as e:
        return f"Error: {e}"


schema = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the root of the project.",
            ),
        },
    ),
)


