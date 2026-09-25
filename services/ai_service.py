import re
from enum import Enum
from openai import OpenAI

class AIService:
    SYSTEM_PROMPT = (
        'You are a funny excuse generator. Based on the situation provided by the user, '
        'generate 3 funny and RELATABLE, REAL-WORLD excuses. '
        'The excuses must be grounded in reality (e.g., traffic, unexpected guests, broken appliances, '
        'pet chaos, slow internet, family drama, or minor daily mishaps). '
        'STRICTLY AVOID all fantasy, sci-fi, or magical themes. '
        'NO dragons, NO portals, NO magic, NO aliens, NO space travel. '
        'Make them funny because they are slightly absurd but actually possible in real life. '
        'Each excuse must be on a single new line. '
        'Each line must start with a dash and a space (e.g., \u0027- \u0027). '
        'Do not include any introduction, any thoughts, or any conclusion. '
        'Just provide the list of 3 excuses.'
    )

    def __init__(self, settings):
        self.settings = settings
        self.client = OpenAI(
            api_key=self.settings.API_KEY,
            base_url=self.settings.BASE_URL,
            timeout=90.0
        )

    def generate_excuses(self, situation: str) -> tuple[str, list[str]]:
        response = self.client.chat.completions.create(
            model=self.settings.MODEL,
            messages=[
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': situation},
            ],
            temperature=0.8,
        )
        
        text = (response.choices[0].message.content or '').strip()
        
        items = []
        for line in text.split('\n'):
            cleaned_line = line.strip()
            if cleaned_line:
                # Remove leading '- ', '1. ', etc.
                cleaned_line = re.sub(r'^\s*(?:\d+[.)]\s*|[-*]\s*)', '', cleaned_line)
                items.append(cleaned_line)
        
        if not items:
            items = [text]
            
        return text, items[:3]

