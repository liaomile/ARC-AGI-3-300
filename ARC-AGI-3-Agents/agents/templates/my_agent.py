"""Public stub — core agent implementation is private.

The competition decision stack (world model, spectral planner,
Flash-Next harness patches, CAM, etc.) is not included here.
"""
from __future__ import annotations

from agents.templates.random_agent import RandomAgent


class MyAgent(RandomAgent):
    """Placeholder agent for local smoke tests only."""


Agent = MyAgent
