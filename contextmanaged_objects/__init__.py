from __future__ import annotations

from abc import ABC
from contextlib import contextmanager
from functools import wraps
from typing import Any

from stringcase import snakecase
from contextmanaged_assign import assign

from inspect_mate_pp import is_regular_method


class HasContextManagedFocus(ABC):
    _CLS_CONTEXT_STACKS: dict[type[HasContextManagedFocus], HasContextManagedFocus] = {}

    @classmethod
    def _name(cls) -> str:
        return snakecase(cls.__name__).strip("_")

    @classmethod
    def _CONTEXT_STACK(cls) -> list[Self]:
        return cls._CLS_CONTEXT_STACKS.setdefault(cls, [])

    @classmethod
    def current(cls) -> Self:
        stack = cls._CONTEXT_STACK()
        if not stack:
            raise RuntimeError(f"No {cls._name()} is currently active")
        return stack[-1]

    @contextmanager
    def as_current(self):
        stack = self._current_stack()
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


class HasContextManagedMethods(HasContextManagedFocus):
    GETATTR_MODE = False

    def __getattribute__(self, __name: str) -> Any:
        if __name == "GETATTR_MODE":
            return super().__getattribute__(__name)
        if self.GETATTR_MODE:
            return super().__getattribute__(__name)

        with assign("self.GETATTR_MODE", True):
            obj = super().__getattribute__(__name)

            if is_regular_method(self.__class__, __name):

                @wraps(obj)
                def wrapper(*args, **kwargs):
                    with self.as_current():
                        return obj(*args, **kwargs)

                obj = wrapper

            return obj


__all__ = ["HasContextManagedFocus", "HasContextManagedMethods"]
