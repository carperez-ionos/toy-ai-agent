from functions.get_file_content import get_file_content

def test_and_print(working_directory, directory):
    print(f"Result for '{directory}' directory:")
    result = get_file_content(working_directory, directory)

    if isinstance(result, str):
        print(f"    {result}")
    else:
        for f in result:
            print(f"    - {f['filename']}: file_size={f['filesize']} bytes, is_dir={f['is_dir']}")

    print()


if __name__ == "__main__":
    test_and_print("calculator", ".")
    test_and_print("calculator", "pkg")
    test_and_print("calculator", "/bin")
    test_and_print("calculator", "../")