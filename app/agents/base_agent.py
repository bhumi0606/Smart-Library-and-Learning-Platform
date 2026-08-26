from openai import AsyncOpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL


class BaseAgent:
    def __init__(
        self,
        name: str,
        system_prompt: str,
        model: str | None = None,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model or OPENAI_CHAT_MODEL

        self.client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.sessions: dict[str, list[dict[str, str]]] = {}

    def _get_history(
        self,
        session_id: str,
    ):
        return self.sessions.setdefault(
            session_id,
            [],
        )

    async def answer(
        self,
        question: str,
        session_id: str,
    ):

        history = self._get_history(
            session_id=session_id,
        )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        answer = response.choices[0].message.content

        history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer

    def clear_session(
        self,
        session_id: str,
    ):

        self.sessions.pop(
            session_id,
            None,
        )
