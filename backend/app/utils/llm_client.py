"""
LLM client wrapper.

Primary path: Anthropic SDK (when LLM_BASE_URL is blank / ANTHROPIC_API_KEY is set).
Fallback path: any OpenAI-compatible gateway (when LLM_BASE_URL is set).

This keeps a single `chat` / `chat_json` interface regardless of the underlying SDK.
"""

import json
import re
from typing import Optional, Dict, Any, List

from ..config import Config


class LLMClient:
    """LLM client. Pass use_report_model=True to use the higher-quality
    synthesis model (Opus) instead of the simulation agent model (sonnet)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        use_report_model: bool = False,
    ):
        self.api_key = api_key or Config.LLM_API_KEY

        raw_base_url = base_url or Config.LLM_BASE_URL
        self.base_url = raw_base_url if raw_base_url else None

        if model:
            self.model = model
        elif use_report_model:
            self.model = Config.LLM_REPORT_MODEL_NAME
        else:
            self.model = Config.LLM_MODEL_NAME

        if not self.api_key:
            raise ValueError("LLM_API_KEY (or ANTHROPIC_API_KEY) is not configured")

        # Route to the right SDK:
        #   - OpenAI-compatible gateway (base_url set) → use openai SDK
        #   - No gateway → use anthropic SDK directly
        if self.base_url:
            from openai import OpenAI
            self._sdk = "openai"
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            import anthropic as _anthropic
            self._sdk = "anthropic"
            self._client = _anthropic.Anthropic(api_key=self.api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
    ) -> str:
        """Send a chat request and return the response text."""
        if self._sdk == "openai":
            return self._chat_openai(messages, temperature, max_tokens, response_format)
        else:
            return self._chat_anthropic(messages, temperature, max_tokens)

    def _chat_openai(self, messages, temperature, max_tokens, response_format):
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format
        response = self._client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content

    def _chat_anthropic(self, messages, temperature, max_tokens):
        # Separate system message from conversation messages (Anthropic API requirement)
        system = ""
        filtered = []
        for m in messages:
            if m.get("role") == "system":
                system = m.get("content", "")
            else:
                filtered.append(m)

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": filtered if filtered else [{"role": "user", "content": "Hello"}],
        }
        if system:
            kwargs["system"] = system

        try:
            response = self._client.messages.create(**kwargs)
        except Exception as e:
            # Some newer models (e.g. opus-4-8) deprecate `temperature` and reject it.
            # Retry once without it.
            if "temperature" in str(e).lower():
                kwargs.pop("temperature", None)
                response = self._client.messages.create(**kwargs)
            else:
                raise
        content = "".join(
            block.text for block in response.content if hasattr(block, "text")
        )
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """Send a chat request and return parsed JSON."""
        # Note: Anthropic does not support response_format={"type":"json_object"};
        # we rely on prompts that enforce JSON output and strip markdown fences.
        response = self.chat(messages=messages, temperature=temperature, max_tokens=max_tokens)
        cleaned = response.strip()
        cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n?```\s*$', '', cleaned)
        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"LLM returned invalid JSON: {cleaned[:200]}")
