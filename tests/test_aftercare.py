"""Tests for aftercare."""

from __future__ import annotations

from aftercare import Aftercare, CleanupResult, __version__


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_reverse_order() -> None:
    order: list[str] = []
    with Aftercare() as ac:
        ac.add(lambda: order.append("close_db"), name="close_db")
        ac.add(lambda: order.append("flush_cache"), name="flush_cache")
    assert order == ["flush_cache", "close_db"]
    assert all(r.ok for r in ac.results)


def test_failed_cleanup_continues() -> None:
    order: list[str] = []

    def boom() -> None:
        order.append("boom")
        raise RuntimeError("fail")

    def later() -> None:
        order.append("later")

    with Aftercare() as ac:
        ac.add(later, name="later")
        ac.add(boom, name="boom")
    # reverse: boom first, then later still runs
    assert order == ["boom", "later"]
    assert len(ac.results) == 2
    by_name = {r.name: r for r in ac.results}
    assert by_name["boom"].ok is False
    assert by_name["later"].ok is True
    assert isinstance(by_name["boom"], CleanupResult)


def test_callback_decorator() -> None:
    order: list[str] = []
    with Aftercare() as ac:

        @ac.callback(name="x")
        def _x() -> None:
            order.append("x")

        ac.add(lambda: order.append("y"), name="y")
    assert order == ["y", "x"]
