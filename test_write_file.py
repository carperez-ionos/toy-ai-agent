from functions.write_file import write_file


def test_and_print(working_directory, file_path, content):
    print(f"Result for '{file_path}':")
    result = write_file(working_directory, file_path, content)
    print(f"    {result}")
    print()


if __name__ == "__main__":
    test_and_print("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    test_and_print("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    test_and_print("calculator", "/tmp/temp.txt", "this should not be allowed")