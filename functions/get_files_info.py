from os import listdir
from os.path import (
        getsize,
        abspath,
        join,
        isdir,
        normpath
        )
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = normpath(join(
                abspath(working_directory), 
                directory
                ))

    def res_fmt(): 
        return ("'" +  directory + "'") if (directory != ".") else "current" 

    header_string = f"Result for {res_fmt()} directory:\n"

    if not full_path.startswith(abspath(working_directory)): 
        return f"{header_string}    Error: Cannot list {directory} as it is outside the permitted working directory"

    if not isdir(full_path):
        return f"{header_string}    Error: {directory} is not a directory"

    try:
        metadata = [] 
        for file in listdir(full_path):
            path = join(full_path, file)
            metadata.append(
                    f"  - {file}: file_size={getsize(path)}, is_dir={isdir(path)}"
                    )
    except Exception as e:
        return f"{header_string}    Error: {e}"

    return f"{header_string}{"\n".join(metadata)}"

schema = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory variable is the relative path from \".\". Therefore to return files at the root, you should input \".\"",
            ),
        },
    ),
)


