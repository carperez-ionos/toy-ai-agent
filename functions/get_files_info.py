import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = ""
        for content in os.listdir(target_dir):
            content_path = os.path.join(target_dir, content)
            size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
            result += f"- {content}: file_size={size}, is_dir={is_dir}\n"

        return result

    except Exception as e:
        return f"Error: {e}"


# Google GenAI schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)