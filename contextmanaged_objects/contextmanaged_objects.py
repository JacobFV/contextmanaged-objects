from __future__ import annotations

from abc import ABC
from contextlib import contextmanager
from functools import wraps
from typing import Any

from stringcase import snakecase
from contextmanaged_assign import assign
from inspect_mate_pp import get_regular_methods


class HasContextManagedFocus(ABC):
    _CLS_CONTEXT_STACKS: dict[type[HasContextManagedFocus], HasContextManagedFocus] = {}

    @classmethod
    def _CONTEXT_STACK(cls) -> list[HasContextManagedFocus]:
        return cls._CLS_CONTEXT_STACKS.setdefault(cls, [])

    @classmethod
    def current(cls) -> HasContextManagedFocus or None:
        """Returns the instance on top of the context stack, or None if the
        context stack is empty."""
        stack = cls._CONTEXT_STACK()
        if not stack:
            return None
        return stack[-1]

    @contextmanager
    def as_current(self):
        """Context manager that puts the instance on top of its context stack"""

        stack = self._CONTEXT_STACK()
        if stack and stack[-1] is self:
            yield
        else:
            stack.append(self)
            try:
                yield
            finally:
                tail = stack.pop()
                if tail is not self:
                    raise RuntimeError(
                        f"Context stack corrupted: expected {self} but got {tail}"
                    )


def make_current():
    """Decorator for instance methods when you want them to automatically
    put the instance on top of its context stack during invokation and
    remove after invokation is over."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            with self.as_current():
                return fn(self, *args, **kwargs)

        return wrapper

    return decorator


__all__ = ["make_current", "HasContextManagedFocus"]
