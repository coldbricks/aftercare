# aftercare

[![PyPI](https://img.shields.io/pypi/v/aftercare.svg)](https://pypi.org/project/aftercare/)
[![Python Versions](https://img.shields.io/pypi/pyversions/aftercare.svg)](https://pypi.org/project/aftercare/)
[![CI](https://github.com/coldbricks/aftercare/actions/workflows/ci.yml/badge.svg)](https://github.com/coldbricks/aftercare/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Teardown orchestration for Python. Register cleanup steps, then run them in reverse order on exit — logging each one's success or failure without short-circuiting the rest.

## Install

```bash
pip install aftercare
```

## Quickstart

```python
from aftercare import Aftercare

order = []
with Aftercare() as ac:
    ac.add(lambda: order.append("close_db"), name="close_db")
    ac.add(lambda: order.append("flush_cache"), name="flush_cache")
    # main work...

assert order == ["flush_cache", "close_db"]
assert all(r.ok for r in ac.results)
```

## Why this exists

- LIFO cleanup matches resource acquisition order
- One failed cleanup does not skip the rest
- Results recorded for ops / tests via `ac.results`

## API

| Symbol | Description |
|--------|-------------|
| `Aftercare` | Context manager for reverse-order cleanup |
| `Aftercare.add(fn, name=...)` | Register a cleanup step |
| `Aftercare.callback(name=...)` | Decorator form of add |
| `CleanupResult` | Per-step name / ok / error |

## Related packages

Part of the coldbricks micro-library suite (small, typed, zero-dependency helpers):

| Package | Role |
|---------|------|
| [`buzzkill`](https://github.com/coldbricks/buzzkill) | Guaranteed shutdown callbacks |
| **aftercare** | Reverse-order teardown |
| [`fluffer`](https://github.com/coldbricks/fluffer) | Startup pre-warm |
| [`edging`](https://github.com/coldbricks/edging) | Token-bucket rate limit |
| [`readback`](https://github.com/coldbricks/readback) | Echo-confirmation validation |
| [`hearback`](https://github.com/coldbricks/hearback) | Output re-validation decorator |
| [`agecheck`](https://github.com/coldbricks/agecheck) | Timezone-correct age thresholds |
| [`transponder`](https://github.com/coldbricks/transponder) | State broadcast on change |

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
mypy src
```

## Roadmap

This is an early **0.1.0** release (Alpha) with active development planned:

- Async cleanup support
- Timeout and cancel policies
- Structured result export for ops tooling

## License

MIT © Coldbricks — coldbricks@gmail.com
