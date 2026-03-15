from functions.get_file_content import get_file_content


def test_and_print(working_directory, file_path):
    print(f"Result for '{file_path}':")
    result = get_file_content(working_directory, file_path)
    print(result)
    print()


if __name__ == "__main__":
    test_and_print("calculator", "lorem.txt")
    test_and_print("calculator", "main.py")
    test_and_print("calculator", "pkg/calculator.py")
    test_and_print("calculator", "/bin/cat")
    test_and_print("calculator", "pkg/does_not_exist.py")