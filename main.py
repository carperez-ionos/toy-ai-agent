import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

MAX_ITERATIONS = 20


def setup_gemini_client(user_api_key: str):
    client = genai.Client(api_key=user_api_key)
    return client


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <user_prompt> [--verbose]")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    user_prompt = sys.argv[1]

    load_dotenv()
    user_api_key = os.environ.get("GEMINI_API_KEY")
    client = setup_gemini_client(user_api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(MAX_ITERATIONS):
        # Send messages to the LLM (every iteration, not just once)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            ),
        )

        if response is None or response.usage_metadata is None:
            print("Response is malformed.")
            return

        if verbose_flag:
            print(f"Iteration {i + 1}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Append the model's response to messages
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        # If the model wants to call functions, execute them and loop
        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose=verbose_flag)
                messages.append(result)
            # Loop continues — next iteration sends updated messages back to LLM

        else:
            # No function calls — the model is done, print final response
            print(response.text)
            return

    print("Max iterations reached.")


if __name__ == "__main__":
    main()