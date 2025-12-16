import subprocess
from os.path import (
        basename,
        abspath,
        join,
        isfile,
        normpath,
        exists
        )

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_path = abspath(working_directory)

    full_path = normpath(join(
                abs_working_path,
                file_path
                ))


    if not full_path.startswith(abs_working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not exists(full_path):
        return f'Error: File "{file_path}" not found'

    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    call = ["python3",full_path] + args
    try:
        p = subprocess.run(call, cwd=working_directory, timeout=30, capture_output=True)

        out = f"STDOUT:{p.stdout}\nSTDERR:{p.stderr}"
        
        if p.returncode != 0:
            out += f"Process exited with code {p.returncode}"

        if p.stdout:
            out += f"\nNo output produced"
            
        return out
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files, returning stdout and stderr, constrained to the working directory.",
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

