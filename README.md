# ARC-AGI-3-300

Partial open-source mirror of an ARC Prize 2026 — ARC-AGI-3 working tree.

> **Core scoring algorithms are private.** See [`SCOPE.md`](SCOPE.md).
> This repo ships scaffolding + stubs so others can study the harness layout
> and run a non-scoring smoke agent.

## What you get

| Path | Contents |
|------|----------|
| `ARC-AGI-3-Agents/` | Agent framework scaffolding (upstream-style) |
| `ARC-AGI-3-Agents/agents/templates/my_agent.py` | **Stub** (random) — not the competition agent |
| `SCOPE.md` | Explicit public / private boundary |
| `NOTICE.md` | Attribution / third-party notes |

## Quick start (smoke only)

```bash
cd ARC-AGI-3-Agents
cp .env.example .env   # add your own keys if you use LLM templates
# follow upstream README for uv/pip install and local play
```

## Results note

Public-leaderboard work from this line reached the **~32 score / top-hundreds**
band on ARC-AGI-3 with a private Flash-Next stack. That stack, patches, and
notebooks are **not** included here.

## License

See `LICENSE` and `NOTICE.md`.
