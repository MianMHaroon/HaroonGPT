from google import genai
from google.genai import types

class LLMClient:
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def ask(self, prompt: str):
        config = types.GenerateContentConfig(
            max_output_tokens=512,
            temperature=0
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )

        if hasattr(response, "text") and response.text:
            return response.text
        return "I'm not sure I understood that, but I'm here to help! Could you rephrase it?"
