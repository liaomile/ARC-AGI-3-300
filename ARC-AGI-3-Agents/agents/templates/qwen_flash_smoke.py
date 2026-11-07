# -*- coding: utf-8 -*-
"""Qwen3.8-Flash cloud API smoke agent for local A/B (not Kaggle Flash-Next)."""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

import openai
from arcengine import FrameData, GameAction
from openai import OpenAI as OpenAIClient

from .llm_agents import FastLLM

logger = logging.getLogger()


class QwenFlashSmoke(FastLLM):
    """FastLLM pointed at Qwen compatible-mode; tool_choice=auto (required is flaky)."""

    MODEL = os.environ.get("LOCAL_SMOKE_MODEL", "qwen3.8-flash")
    MODEL_REQUIRES_TOOLS = True
    DO_OBSERVATION = False  # fewer round-trips for smoke

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        try:
            self.MAX_ACTIONS = int(os.environ.get("LOCAL_SMOKE_MAX_ACTIONS", "40"))
        except ValueError:
            self.MAX_ACTIONS = 40

    def _client(self) -> OpenAIClient:
        return OpenAIClient(
            api_key=os.environ.get("OPENAI_API_KEY")
            or os.environ.get("DASHSCOPE_API_KEY")
            or "",
            base_url=os.environ.get("OPENAI_BASE_URL")
            or os.environ.get("LOCAL_ANALYZER_BASE_URL")
            or None,
        )

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        logging.getLogger("openai").setLevel(logging.CRITICAL)
        logging.getLogger("httpx").setLevel(logging.CRITICAL)
        client = self._client()
        tools = self.build_tools()

        if len(self.messages) == 0:
            user_prompt = self.build_user_prompt(latest_frame)
            self.push_message({"role": "user", "content": user_prompt})
            self.push_message(
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": self._latest_tool_call_id,
                            "type": "function",
                            "function": {
                                "name": GameAction.RESET.name,
                                "arguments": json.dumps({}),
                            },
                        }
                    ],
                }
            )
            return GameAction.RESET

        function_response = self.build_func_resp_prompt(latest_frame)
        self.push_message(
            {
                "role": "tool",
                "tool_call_id": self._latest_tool_call_id,
                "content": str(function_response),
            }
        )
        user_prompt = self.build_user_prompt(latest_frame)
        self.push_message({"role": "user", "content": user_prompt})

        name = GameAction.ACTION5.name
        arguments: Optional[str] = None
        try:
            response = client.chat.completions.create(
                model=self.MODEL,
                messages=self.messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024,
                extra_body={"enable_thinking": False},
            )
        except openai.BadRequestError as e:
            logger.info("Message dump: %s", self.messages)
            raise e

        self.track_tokens(response.usage.total_tokens if response.usage else 0)
        message5 = response.choices[0].message
        if message5.tool_calls:
            tool_call = message5.tool_calls[0]
            self._latest_tool_call_id = tool_call.id
            name = tool_call.function.name
            arguments = tool_call.function.arguments
            self.push_message(message5)
        else:
            # fallback: model answered in text — RESET-safe ACTION5
            self.push_message(
                {
                    "role": "assistant",
                    "content": message5.content or "(no tool call)",
                }
            )
            logger.info("No tool_calls; default ACTION5. content=%r", message5.content)

        action = GameAction.from_name(name)
        try:
            action.set_data(
                json.loads(arguments)
                if isinstance(arguments, (str, bytes, bytearray)) and arguments
                else (arguments or {})
            )
        except Exception:
            action.set_data({})
        return action
