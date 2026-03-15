from functions import function_map


def call_function(function_name: str, args: dict, working_directory: str, verbose: bool = False):
    if verbose:
        print(f"Calling function: {function_name}({args})")
    print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {"error": f"Unknown function: {function_name}"}

    args["working_directory"] = working_directory
    result = function_map[function_name](**args)
    return {"result": result}
