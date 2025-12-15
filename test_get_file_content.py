from functions.get_file_content import get_file_content

print(f"test 1: {get_file_content("calculator", "lorem.txt")}")
print(f"test 1: {get_file_content("calculator", "main.py")}")
print(f"test 2: {get_file_content("calculator", "pkg/calculator.py")}")
print(f"test 3: {get_file_content("calculator", "/bin/cat")}")
print(f"test 1: {get_file_content("calculator", "pkg/does_not_exist.py")}")
