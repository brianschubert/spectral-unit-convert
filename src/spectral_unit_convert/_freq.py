from __future__ import annotations

import abc
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Final,
    Generic,
    Literal,
    TypeVar,
    Union,
    overload,
)

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from ._typing import SupportsFloatDivMul


_T = TypeVar("_T", bound="SupportsFloatDivMul")

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
    "A",  # Unique to wavelength: angstroms.
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

SPEED_OF_LIGHT: Final = 299_792_458.0


class _FrequencyMeasure(Generic[_T], abc.ABC):
    # Value expressed in base units is equal to `_value * 10 ** _scale`
    _value: _T
    _scale: int

    _SCALES: ClassVar[
        dict[_UNIT_FREQUENCY, int]
        | dict[_UNIT_WAVELENGTH, int]
        | dict[_UNIT_WAVENUMBER, int]
    ]

    __slots__ = ("_value", "_scale")

    def __init_subclass__(
        cls, *, unit_suffix: str, invert: bool = False, **kwargs: Any
    ) -> None:
        super().__init_subclass__(**kwargs)

        sign = -1 if invert else 1
        cls._SCALES = {  # type: ignore[assignment]
            f"{prefix}{unit_suffix}": sign * scale
            for prefix, scale in _PREFIX_SCALES.items()
        }

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({self.value!r}, {self.unit!r})"

    @property
    def value(self) -> _T:
        return self._value

    @property
    def scale(self) -> int:
        return self._scale

    @property
    def unit(self) -> _UNIT_FREQUENCY | _UNIT_WAVELENGTH | _UNIT_WAVENUMBER:
        return next(
            iter(
                symbol for symbol, scale in self._SCALES.items() if scale == self._scale
            )
        )

    def as_frequency(self, unit: _UNIT_FREQUENCY) -> Frequency[_T]:
        return Frequency(self.value_as_frequency(unit), unit)

    def as_wavelength(self, unit: _UNIT_WAVELENGTH) -> Wavelength[_T]:
        return Wavelength(self.value_as_wavelength(unit), unit)

    def as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> Wavenumber[_T]:
        return Wavenumber(self.value_as_wavenumber(unit), unit)

    @overload
    def as_unit(
        self,
        measure: type[Frequency[_T]],
        unit: _UNIT_FREQUENCY,
    ) -> Frequency[_T]: ...

    @overload
    def as_unit(
        self,
        measure: type[Wavelength[_T]],
        unit: _UNIT_WAVELENGTH,
    ) -> Wavelength[_T]: ...

    @overload
    def as_unit(
        self,
        measure: type[Wavenumber[_T]],
        unit: _UNIT_WAVENUMBER,
    ) -> Wavenumber[_T]: ...

    def as_unit(
        self,
        measure: type[FrequencyMeasure[_T]],
        unit: _UNIT_FREQUENCY | _UNIT_WAVELENGTH | _UNIT_WAVENUMBER,
    ) -> FrequencyMeasure[_T]:
        converter_lookup = {
            Frequency: self.as_frequency,
            Wavelength: self.as_wavelength,
            Wavenumber: self.as_wavenumber,
        }
        return converter_lookup[measure](unit)  # type: ignore

    @abc.abstractmethod
    def value_as_frequency(self, unit: _UNIT_FREQUENCY) -> _T: ...

    @abc.abstractmethod
    def value_as_wavelength(self, unit: _UNIT_WAVELENGTH) -> _T: ...

    @abc.abstractmethod
    def value_as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> _T: ...


class Frequency(_FrequencyMeasure[_T], unit_suffix="Hz"):
    """
    >>> Frequency(2.4, "GHz").as_wavelength("cm")
    Wavelength(12.49..., 'cm')
    >>> Frequency(2.4, "GHz").as_wavenumber("cm-1").as_wavelength("cm")
    Wavelength(12.49..., 'cm')
    >>> Frequency(1000.0, "MHz").as_frequency("GHz")
    Frequency(1.0, 'GHz')
    """

    __slots__ = ()

    _SCALES: ClassVar[dict[_UNIT_FREQUENCY, int]]

    def __init__(self, value: _T, unit: _UNIT_FREQUENCY) -> None:
        self._value = value
        self._scale = self._SCALES[unit]

    def value_as_frequency(self, unit: _UNIT_FREQUENCY) -> _T:
        dest_scale = Frequency._SCALES[unit]
        return self.value * 10.0 ** (self._scale - dest_scale)

    def value_as_wavelength(self, unit: _UNIT_WAVELENGTH) -> _T:
        dest_scale = Wavelength._SCALES[unit]
        return SPEED_OF_LIGHT / self.value * 10.0 ** (-dest_scale - self._scale)

    def value_as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> _T:
        dest_scale = Wavenumber._SCALES[unit]
        return self.value / SPEED_OF_LIGHT * 10.0 ** (-dest_scale + self._scale)


class Wavelength(_FrequencyMeasure[_T], unit_suffix="m"):
    """
    >>> Wavelength(12.49, 'cm').as_frequency("GHz")
    Frequency(2.4..., 'GHz')
    >>> Wavelength(2.5, 'um').as_wavenumber("cm-1")
    Wavenumber(4000.0, 'cm-1')
    >>> Wavelength(1.0, 'nm').as_wavelength("A")
    Wavelength(10.0, 'A')
    """

    __slots__ = ()

    _SCALES: ClassVar[dict[_UNIT_WAVELENGTH, int]]

    def __init__(self, value: _T, unit: _UNIT_WAVELENGTH) -> None:
        self._value = value
        self._scale = self._SCALES[unit]

    def value_as_frequency(self, unit: _UNIT_FREQUENCY) -> _T:
        dest_scale = Frequency._SCALES[unit]
        return SPEED_OF_LIGHT / self.value * 10.0 ** (-dest_scale - self._scale)

    def value_as_wavelength(self, unit: _UNIT_WAVELENGTH) -> _T:
        dest_scale = Wavelength._SCALES[unit]
        return self.value * 10.0 ** (self._scale - dest_scale)

    def value_as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> _T:
        dest_scale = Wavenumber._SCALES[unit]
        return 1 / self.value * 10.0 ** (-dest_scale - self._scale)


Wavelength._SCALES["A"] = -10  # Unique to wavelength: angstroms.


class Wavenumber(_FrequencyMeasure[_T], unit_suffix="m-1", invert=True):
    """
    >>> Wavenumber(4000.0, 'cm-1').as_wavelength("um")
    Wavelength(2.5, 'um')
    >>> Wavenumber(4000.0, 'cm-1').as_frequency("GHz").as_wavelength("um")
    Wavelength(2.5..., 'um')
    """

    __slots__ = ()

    _SCALES: ClassVar[dict[_UNIT_WAVENUMBER, int]]

    def __init__(self, value: _T, unit: _UNIT_WAVENUMBER) -> None:
        self._value = value
        self._scale = self._SCALES[unit]

    def value_as_frequency(self, unit: _UNIT_FREQUENCY) -> _T:
        dest_scale = Frequency._SCALES[unit]
        return SPEED_OF_LIGHT * self.value * 10.0 ** (-dest_scale + self._scale)

    def value_as_wavelength(self, unit: _UNIT_WAVELENGTH) -> _T:
        dest_scale = Wavelength._SCALES[unit]
        return 1 / self.value * 10.0 ** (-dest_scale - self._scale)

    def value_as_wavenumber(self, unit: _UNIT_WAVENUMBER) -> _T:
        dest_scale = Wavenumber._SCALES[unit]
        return self.value * 10.0 ** (self._scale - dest_scale)
