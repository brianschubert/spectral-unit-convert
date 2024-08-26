from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Final, Generic, Literal, TypeVar, Union

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

_T = TypeVar("_T")

_UNIT_PREFIX: TypeAlias = Literal[
    "P", "T", "G", "M", "k", "-", "c", "m", "u", "n", "p", "f"
]

_UNIT_FREQUENCY: TypeAlias = Literal[
    "PHz",
    "THz",
    "GHz",
    "MHz",
    "kHz",
    "-Hz",
    "cHz",
    "mHz",
    "uHz",
    "nHz",
    "pHz",
    "fHz",
]
_UNIT_WAVELENGTH: TypeAlias = Literal[
    "Pm",
    "Tm",
    "Gm",
    "Mm",
    "km",
    "-m",
    "cm",
    "mm",
    "um",
    "nm",
    "pm",
    "fm",
]

_UNIT_WAVENUMBER: TypeAlias = Literal[
    "Pm-1",
    "Tm-1",
    "Gm-1",
    "Mm-1",
    "km-1",
    "-m-1",
    "cm-1",
    "mm-1",
    "um-1",
    "nm-1",
    "pm-1",
    "fm-1",
]

FrequencyMeasure: TypeAlias = Union["Frequency[_T]", "Wavelength[_T]", "Wavenumber[_T]"]

_PREFIX_SCALES: Final[dict[_UNIT_PREFIX, int]] = {
    "P": 15,
    "T": 12,
    "G": 9,
    "M": 6,
    "k": 3,
    "-": 0,
    "c": -2,
    "m": -3,
    "u": -6,
    "n": -9,
    "p": -12,
    "f": -15,
}


class _FrequencyMeasure(Generic[_T], abc.ABC):
    _value: _T
    _scale: int

    __slots__ = ("_value", "_scale")

    @abc.abstractmethod
    def as_frequency(self, unit: _UNIT_FREQUENCY) -> Frequency[_T]: ...

    @abc.abstractmethod
    def as_wavelength(self, unit: _UNIT_WAVELENGTH) -> Wavelength[_T]: ...

    @abc.abstractmethod
    def as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> Wavenumber[_T]: ...


class Frequency(_FrequencyMeasure[_T]):
    __slots__ = ()


class Wavelength(_FrequencyMeasure[_T]):
    __slots__ = ()


class Wavenumber(_FrequencyMeasure[_T]):
    __slots__ = ()
