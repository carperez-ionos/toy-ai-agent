from google import genai
from google.genai import types
from .base import Agent
from schemas.gemini import available_functions
from call_function import call_function
from config import WORKING_DIRECTORY


class GeminiAgent(Agent):
    def _build_client(self):
        return genai.Client(api_key=self.api_key)

    def _build_initial_messages(self, user_prompt: str) -> list:
        return [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    def _send(self, messages: list):
        return self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=self.temperature,
                tools=[available_functions],
            ),
        )

    def _append_response(self, messages, response):
        if response.candidates:
            for candidate in response.candidates:
                if candidate and candidate.content:
                    messages.append(candidate.content)
        return messages

    def _get_tool_calls(self, response):
        return response.function_calls or None

    def _execute_tool_call(self, tool_call):
        result = call_function(
            function_name=tool_call.name,
            args=dict(tool_call.args) if tool_call.args else {},
            working_directory=WORKING_DIRECTORY,
            verbose=self.verbose,
        )
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=tool_call.name,
                    response=result,
                )
            ],
        )

    def _append_tool_result(self, messages, result):
        messages.append(result)
        return messages

    def _get_text(self, response):
        return response.text

    def _log_usage(self, response, iteration):
        if response.usage_metadata:
            print(f"Iteration {iteration}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")