from typing import Type, cast
import importlib

from dotenv import load_dotenv

from .agent import Agent, Playback
from .recorder import Recorder
from .swarm import Swarm
from .templates.random_agent import Random
from .templates.my_agent import MyAgent
from .templates.lingjing_solo_agent import LingjingSolo

load_dotenv()

AVAILABLE_AGENTS: dict[str, Type[Agent]] = {
    cls.__name__.lower(): cast(Type[Agent], cls)
    for cls in Agent.__subclasses__()
    if cls.__name__ != "Playback"
}

for rec in Recorder.list():
    AVAILABLE_AGENTS[rec] = Playback

AVAILABLE_AGENTS["myagent"] = MyAgent
AVAILABLE_AGENTS["aether"] = MyAgent
AVAILABLE_AGENTS["lingjingsolo"] = LingjingSolo
AVAILABLE_AGENTS["lingjing"] = LingjingSolo
# registered via optional import below as qwenflashsmoke

# Optional heavy deps (langchain/langgraph/smolagents) — skip if missing.
_OPTIONAL = [
    ("LangGraphFunc", ".templates.langgraph_functional_agent"),
    ("LangGraphTextOnly", ".templates.langgraph_functional_agent"),
    ("LangGraphRandom", ".templates.langgraph_random_agent"),
    ("LangGraphThinking", ".templates.langgraph_thinking"),
    ("LLM", ".templates.llm_agents"),
    ("FastLLM", ".templates.llm_agents"),
    ("GuidedLLM", ".templates.llm_agents"),
    ("ReasoningLLM", ".templates.llm_agents"),
    ("MultiModalLLM", ".templates.multimodal"),
    ("OpenClaw", ".templates.openclaw_agent"),
    ("ReasoningAgent", ".templates.reasoning_agent"),
    ("SmolCodingAgent", ".templates.smolagents"),
    ("SmolVisionAgent", ".templates.smolagents"),
    ("QwenFlashSmoke", ".templates.qwen_flash_smoke"),
]
for _name, _mod in _OPTIONAL:
    try:
        mod = importlib.import_module(_mod, package=__package__)
        cls = getattr(mod, _name)
        AVAILABLE_AGENTS[_name.lower()] = cast(Type[Agent], cls)
        globals()[_name] = cls
    except Exception:
        pass

__all__ = [
    "Swarm",
    "Random",
    "MyAgent",
    "LingjingSolo",
    "Agent",
    "Recorder",
    "Playback",
    "AVAILABLE_AGENTS",
]
