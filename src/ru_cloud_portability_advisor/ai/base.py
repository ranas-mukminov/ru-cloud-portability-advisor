from __future__ import annotations

from typing import Protocol


class AIProvider(Protocol):
    def complete(self, prompt: str) -> str:
        ...

    def chat(self, messages: list[dict]) -> str:
        ...


class NoopAIProvider:
    """A placeholder AI provider returning stub responses."""

    def complete(self, prompt: str) -> str:
        return "AI provider is not configured. Provide your own implementation."

    def chat(self, messages: list[dict]) -> str:
        return "AI provider is not configured. Provide your own implementation."

