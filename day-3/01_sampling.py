import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt = """
Give one short creative name for a personal finance application.

Return only the name.
"""


def run_experiment(temperature, runs=5):
    print(f"\n===== TEMPERATURE {temperature} =====")

    for i in range(1, runs + 1):
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "temperature": temperature
            }
        )

        print(f"Run {i}: {response.text.strip()}")


run_experiment(0)
run_experiment(1)