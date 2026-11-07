# Open-source scope

## Published
- High-level project README and run instructions
- Official-style agent **scaffolding** under `ARC-AGI-3-Agents/`
  (entrypoints, random/LLM templates, generic strategy base)
- `.env.example` (no secrets)
- Stub `agents/templates/my_agent.py` for smoke tests

## Not published (core / private)
- Competition decision stack and world-model / spectral / planner code (`lingjing_solo`, lincore)
- Flash-Next / Pennyroyal campaign notebooks, patches, and score ledgers
- CAM / memento / engine-solver ports
- Game-specific probe & run strategies
- lingjing_solo_agent adapter and related contract tests
- Kaggle credentials, API keys, `.env`, runtime logs, recordings
- Full third-party winning submissions (link upstream instead)

The private stack that produced the ~32 public-band / top-hundreds result
is not in this repository.
