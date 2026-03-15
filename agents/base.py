from abc import ABC, abstractmethod
from config import MAX_ITERATIONS, DEFAULT_TEMPERATURE, MAX_CONTEXT_MESSAGES


class Agent(ABC):
    def __init__(
        self,
        api_key: str,
        system_prompt: str,
        tools: list,
        verbose: bool = False,
        temperature: float = DEFAULT_TEMPERATURE,
        max_iterations: int = MAX_ITERATIONS,
        max_context_messages: int = MAX_CONTEXT_MESSAGES,
    ):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.tools = tools
        self.verbose = verbose
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.max_context_messages = max_context_messages
        self.client = self._build_client()

    @abstractmethod
    def _build_client(self):
        pass

    @abstractmethod
    def _build_initial_messages(self, user_prompt: str) -> list:
        pass

    @abstractmethod
    def _send(self, messages: list):
        pass

    @abstractmethod
    def _append_response(self, messages: list, response) -> list:
        pass

    @abstractmethod
    def _get_tool_calls(self, response) -> list | None:
        pass

    @abstractmethod
    def _execute_tool_call(self, tool_call) -> object:
        pass

    @abstractmethod
    def _append_tool_result(self, messages: list, result) -> list:
        pass

    @abstractmethod
    def _get_text(self, response) -> str:
        pass

    @abstractmethod
    def _log_usage(self, response, iteration: int):
        pass

    def _trim_context(self, messages: list) -> list:
        """Keep the first message (user prompt) and the most recent messages."""
        if len(messages) <= self.max_context_messages:
            return messages
        first_message = messages[0]
        recent_messages = messages[-(self.max_context_messages - 1):]
        return [first_message] + recent_messages

    def run(self, user_prompt: str) -> str:
        messages = self._build_initial_messages(user_prompt)

        for i in range(self.max_iterations):
            messages = self._trim_context(messages)
            response = self._send(messages)

            if response is None:
                return "Response is malformed."

            if self.verbose:
                self._log_usage(response, i + 1)

            messages = self._append_response(messages, response)

            tool_calls = self._get_tool_calls(response)
            if tool_calls:
                for tool_call in tool_calls:
                    result = self._execute_tool_call(tool_call)
                    messages = self._append_tool_result(messages, result)
            else:
                return self._get_text(response)

        return "Max iterations reached."