from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing_extensions import Self


class SupportsFloatDivMul(Protocol):
    def __truediv__(self, other: float | Self) -> Self: ...

    def __rtruediv__(self, other: float | Self) -> Self: ...

    def __mul__(self, other: float | Self) -> Self: ...

    def __rmul__(self, other: float | Self) -> Self: ...
