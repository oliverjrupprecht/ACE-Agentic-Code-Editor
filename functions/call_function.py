from google.genai import types

from working_directory import working_directory
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    args = function_call_part.args
    name = function_call_part.name

    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    func_dict = {"get_files_info" : get_files_info,
                 "get_file_content" : get_file_content,
                 "run_python_file" : run_python_file,
                 "write_file" : write_file
                 }

    call_args = {
            **dict(args),
            "working_directory" : working_directory
            }

    if name in func_dict:
        function = func_dict[name]
        output = function(**call_args)

        return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"result": output},
                            )
                        ],
                    )
    else:
        return types.Content(role="tool",
                            parts=[types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"error": f"Unknown function: {function_call_part.name}"},
                            )
                        ],
                    ) 
