from functions.run_python_file import run_python_file


print(f'test 1:{run_python_file("calculator", "main.py")}\n') 
print(f'test 2:{run_python_file("calculator", "main.py", ["3 + 5"])}\n') 
print(f'test 3:{run_python_file("calculator", "tests.py")}\n') 
print(f'test 4:{run_python_file("calculator", "../main.py")}\n') 
print(f'test 5:{run_python_file("calculator", "nonexistent.py")}\n') 
print(f'test 6:{run_python_file("calculator", "lorem.txt")}\n') 
