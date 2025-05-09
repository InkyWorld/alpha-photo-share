import os
import random
from faker import Faker

def generate_dummy_files(directory, num_files=4096):
    """
    Generates dummy Python files with random content in a specified directory,
    and creates an __init__.py file to import them.

    Args:
        directory (str): The directory where the files will be created.
        num_files (int): The number of dummy files to generate (default is 65536).
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    fake = Faker()

    with open(os.path.join(directory, "__init__.py"), "w") as init_file:
        for i in range(num_files):
            filename = f"{i:04x}.py"
            filepath = os.path.join(directory, filename)

            content_size = random.randint(1024, 2048)  # 1KB to 2KB
            # Generate random Python code
            content = generate_python_code(fake, content_size)

            with open(filepath, "w") as dummy_file:
                dummy_file.write(f"# {filename}\n")
                dummy_file.write(content)

            module_name = filename[:-3]  # Remove ".py" extension
            init_file.write(f"from . import {module_name}\n")

def generate_python_code(fake, size):
    """Generates random Python code."""
    code = ""
    while len(code) < size:
        # Add some random function definitions, variable assignments, or comments
        choice = random.randint(0, 2)
        if choice == 0:
            # Function definition
            func_name = fake.word()
            arg1 = fake.word()
            arg2 = fake.word()
            code += f"def {func_name}({arg1}, {arg2}):\n    return {arg1} + {arg2}\n\n"
        elif choice == 1:
            # Variable assignment
            var_name = fake.word()
            value = random.randint(1, 100)
            code += f"{var_name} = {value}\n"
        else:
            # Comment
            code += f"# {fake.sentence()}\n"
    return code

if __name__ == "__main__":
    output_directory = "genlib"  # You can change this name
    generate_dummy_files(output_directory)
    print(f"Generated dummy files in '{output_directory}' directory.")