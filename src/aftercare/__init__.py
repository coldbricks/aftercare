"""aftercare: teardown orchestration with reverse-order cleanup logging."""

from __future__ import annotations

import logging
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from types import TracebackType
from typing import Callable, List, Literal, Optional, Type

__all__ = ["Aftercare", "CleanupResult"]
__version__ = "0.1.0"

CleanupFn = Callable[[], None]
log = logging.getLogger("aftercare")


@dataclass
class CleanupResult:
    name: str
    ok: bool
    error: Optional[BaseException] = None


@dataclass
class Aftercare(AbstractContextManager["Aftercare"]):
    """Exit-stack style wrapper that runs cleanup steps in reverse order.

    Each step's success or failure is recorded and logged. Failures in one
    cleanup do not prevent subsequent (earlier-registered) cleanups from running.
    """

    _steps: List[tuple[str, CleanupFn]] = field(default_factory=list)
    results: List[CleanupResult] = field(default_factory=list)
    logger: logging.Logger = field(default=log)

    def add(self, fn: CleanupFn, name: Optional[str] = None) -> "Aftercare":
        label: str = name if name is not None else str(getattr(fn, "__name__", "cleanup"))
        self._steps.append((label, fn))
        return self

    def callback(self, name: Optional[str] = None) -> Callable[[CleanupFn], CleanupFn]:
        """Decorator form of :meth:`add`."""

        def deco(fn: CleanupFn) -> CleanupFn:
            self.add(fn, name=name)
            return fn

        return deco

    def __enter__(self) -> Aftercare:
        self.results = []
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.results = []
        for name, fn in reversed(self._steps):
            try:
                fn()
            except BaseException as err:  # noqa: BLE001 — record and continue
                self.results.append(CleanupResult(name=name, ok=False, error=err))
                self.logger.error("aftercare cleanup %r failed: %s", name, err)
            else:
                self.results.append(CleanupResult(name=name, ok=True))
                self.logger.info("aftercare cleanup %r ok", name)
        return False
