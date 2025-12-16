import os
from typing_extensions import get_overloads 
from dotenv import load_dotenv
from google.genai import (
    client,
    types
) 

from functions.get_files_info import schema_get_files_info
from functions import (
        get_files_info as fi,
        get_file_content as fc,
        run_python_file as rp,
        write_file as wf
        )

from functions.call_function import call_function

from prompts import system_prompt
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") 

if api_key == None:
    raise RuntimeError("API key could not be found")

client = client.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

available_functions = types.Tool(
        function_declarations=[fi.schema_get_files_info, fc.schema_get_file_content, rp.schema_run_python_file, wf.schema_write_file],
        )

response = client.models.generate_content(
    model='gemini-2.5-flash-lite', contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

if response.usage_metadata == None:
    raise RuntimeError("No usage metadata, probably bad request")

functions_called = response.function_calls
is_verbose = args.verbose
call_responses = []

if functions_called:
    for call in functions_called:
        function_call_result = call_function(call, is_verbose)
        fun_response = function_call_result.parts[0].function_response.response

        if not fun_response:
            raise Exception("No output from function")

        call_responses.append(function_call_result.parts[0])

        if is_verbose:
            print(f"-> {fun_response}")

    if args.verbose:
        print(f"""
        User prompt: {args.user_prompt}
        Response tokens: {response.usage_metadata.candidates_token_count}
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response: {[part.function_response.response for part in call_responses]} 
              """)
