import asyncio
import httpx
from typing import List, Optional, Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from core.http_helper import HttpHelper
from pydantic import Field

class SelfHostedLLM(BaseChatModel):
    api_url: str = Field(...)
    api_key: str = Field(...)
    model: str = Field(...)

    @property
    def _llm_type(self) -> str:
        return "self_hosted"

    def _generate(
        self, messages: List[HumanMessage], stop: Optional[List[str]] = None, **kwargs: Any
    ) -> ChatResult:
        formatted_messages = [
            {"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
            for msg in messages
        ]
        # print("formatted_messages")
        # print(formatted_messages)
        # print(self.api_url)
        payload = {"model": self.model, "messages": formatted_messages}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = HttpHelper.post(
    url=self.api_url,
    payload=payload,
    headers=headers
)
        # print("DEBUG RAW RESPONSE:", data)
        content =  data["choices"][0]["message"]["content"]
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])
    def predict(self, text: str) -> str:
        """
        Simple helper to send a single user message and get raw text back.
        """
        chat_result = self._generate([HumanMessage(content=text)])
        return chat_result.generations[0].message.content
