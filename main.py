import os
import sys
from dotenv import load_dotenv
from prompts import system_prompt
from agents import GeminiAgent


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <user_prompt> [--verbose]")
        sys.exit(1)

    verbose_flag = "--verbose" in sys.argv
    user_prompt = sys.argv[1]

    load_dotenv()

    agent = GeminiAgent(
        api_key=os.environ.get("GEMINI_API_KEY"),
        system_prompt=system_prompt,
        tools=[],
        verbose=verbose_flag,
    )

    result = agent.run(user_prompt)
    print(result)


if __name__ == "__main__":
    main()
