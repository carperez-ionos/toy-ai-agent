import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

        if os.path.commonpath([absolute_path, target_dir]) != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Failed to write to a file: {e}"


# Google GenAI schema
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)