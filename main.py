import os
from dotenv import load_dotenv
import argparse
from functions.call_function import call_function
from config import system_prompt

from google.genai import (
    client,
    types
) 
from functions import (
    get_files_info,
    get_file_content,
    run_python_file,
    write_file
)

# load api key into client object 
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") 
if api_key == None:
    raise RuntimeError("API key could not be found")
client = client.Client(api_key=api_key)

# initialise parser
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# insert prompt into content type
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# provide the llm with context on how to call the functions provided to it
available_functions = types.Tool(
        function_declarations=[get_files_info.schema, get_file_content.schema, run_python_file.schema, write_file.schema],
        )

# call the api with the sys prompt, user prompt and available functions
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
    # call each function the llm requested
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
