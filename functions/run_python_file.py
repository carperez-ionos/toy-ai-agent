import subprocess
import os


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None):
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

    if os.path.commonpath([absolute_path, target_dir]) != absolute_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_dir]

    if args:
        command.extend(args)

    try:
        result_object = subprocess.run(
            command,
            cwd=absolute_path,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

        if result_object.returncode != 0:
            return f"Process exited with code {result_object.returncode}"

        if not result_object.stdout and not result_object.stderr:
            return "No output produced."

        output = ""
        if result_object.stdout:
            output += f"STDOUT:\n{result_object.stdout}"
        if result_object.stderr:
            output += f"STDERR:\n{result_object.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
