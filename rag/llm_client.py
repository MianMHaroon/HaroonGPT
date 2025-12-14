import time
from google import genai
from google.genai import types, errors


class LLMClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def _is_complete(self, text: str) -> bool:
        if not text:
            return False

        text = text.strip()
        complete_endings = (".", "?", "!", '"', "'", "”", "’", ")", "]", "}")
        return text.endswith(complete_endings)

    def ask(self, prompt: str, attempt: int = 1, last_text: str | None = None) -> str:
        if attempt > 5:
            return last_text or "⚠️ Service is temporarily unavailable. This may be due to exceeding his LLM plan’s request limit or a network connection issue. Please check your internet and try again shortly."
        config = types.GenerateContentConfig(
            max_output_tokens=512,
            temperature=0
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            text = getattr(response, "text", None)
            if text and self._is_complete(text):
                return text
            
            time.sleep(0.5 * attempt)  
            return self.ask(prompt, attempt + 1, text or last_text)

        except errors.ClientError as e:
            time.sleep(0.5 * attempt)
            return self.ask(prompt, attempt + 1, last_text)
        except Exception:
            time.sleep(0.5 * attempt)
            return self.ask(prompt, attempt + 1, last_text)

