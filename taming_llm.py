import os
from dotenv import load_dotenv
import groq

class LLMClient:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("GROQ_API_KEY")  # Get the API key
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama3-70b-8192"  # or another Groq model

    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None

# Testing the API connection
if __name__ == "__main__":
    client = LLMClient()
    result = client.complete("Hello, how are you?")
    print(result)