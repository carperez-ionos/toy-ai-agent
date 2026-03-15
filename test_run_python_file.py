from functions.run_python_file import run_python_file


def test_and_print(working_directory, file_path, args=None):
    print(f"Result for '{file_path}' (args={args}):")
    result = run_python_file(working_directory, file_path, args)
    print(result)
    print()


if __name__ == "__main__":
    test_and_print("calculator", "main.py")
    test_and_print("calculator", "main.py", ["3 + 5"])
    test_and_print("calculator", "tests.py")
    test_and_print("calculator", "../main.py")
    test_and_print("calculator", "nonexistent.py")
    test_and_print("calculator", "lorem.txt")