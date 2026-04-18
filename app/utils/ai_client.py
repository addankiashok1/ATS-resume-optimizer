import openai
from typing import Any
from app.config.settings import settings


class AIClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set for AI optimization.")

        openai.api_key = self.api_key
        self.model = settings.OPENAI_MODEL
        self.temperature = float(settings.OPENAI_TEMPERATURE)
        self.top_p = float(settings.OPENAI_TOP_P)
        self.max_tokens = int(settings.OPENAI_MAX_TOKENS)

    def complete(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a strict resume optimization assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
        )
        choice = response.choices[0]
        return choice.message.content.strip()
