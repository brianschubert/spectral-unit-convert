from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, overload

from . import Frequency, Wavelength, Wavenumber

if TYPE_CHECKING:
    from ._frequency import (
        _UNIT_FREQUENCY,
        _UNIT_WAVELENGTH,
        _UNIT_WAVENUMBER,
        FrequencyMeasure,
    )
    from ._typing import SupportsFloatDivMul

_T = TypeVar("_T", bound="SupportsFloatDivMul")


class SpectralRadiance(Generic[_T]):
    _spectrum: _T
    _bands: FrequencyMeasure[_T]

    __slots__ = ("_spectrum", "_bands")

    def __init__(self, spectrum: _T, bands: FrequencyMeasure[_T]) -> None:
        self._spectrum = spectrum
        self._bands = bands

    @property
    def spectrum(self) -> _T:
        return self._spectrum

    @property
    def bands(self) -> FrequencyMeasure[_T]:
        return self._bands

    def over_frequency(self, unit: _UNIT_FREQUENCY) -> SpectralRadiance[_T]:
        return SpectralRadiance(
            self.spectrum_over_frequency(unit), self.bands.as_frequency(unit)
        )

    def over_wavelength(self, unit: _UNIT_WAVELENGTH) -> SpectralRadiance[_T]:
        return SpectralRadiance(
            self.spectrum_over_wavelength(unit), self.bands.as_wavelength(unit)
        )

    def over_wavenumber(self, unit: _UNIT_WAVENUMBER) -> SpectralRadiance[_T]:
        return SpectralRadiance(
            self.spectrum_over_wavenumber(unit), self.bands.as_wavenumber(unit)
        )

    @overload
    def over_unit(
        self,
        measure: type[Frequency[_T]],
        unit: _UNIT_FREQUENCY,
    ) -> SpectralRadiance[_T]: ...

    @overload
    def over_unit(
        self,
        measure: type[Wavelength[_T]],
        unit: _UNIT_WAVELENGTH,
    ) -> SpectralRadiance[_T]: ...

    @overload
    def over_unit(
        self,
        measure: type[Wavenumber[_T]],
        unit: _UNIT_WAVENUMBER,
    ) -> SpectralRadiance[_T]: ...

    def over_unit(
        self,
        measure: type[FrequencyMeasure[_T]],
        unit: _UNIT_FREQUENCY | _UNIT_WAVELENGTH | _UNIT_WAVENUMBER,
    ) -> SpectralRadiance[_T]:
        converter_lookup = {
            Frequency: self.over_frequency,
            Wavelength: self.over_wavelength,
            Wavenumber: self.over_wavenumber,
        }
        return converter_lookup[measure](unit)  # type: ignore

    def spectrum_over_frequency(self, unit: _UNIT_FREQUENCY) -> _T:
        raise NotImplementedError

    def spectrum_over_wavelength(self, unit: _UNIT_WAVELENGTH) -> _T:
        raise NotImplementedError

    def spectrum_over_wavenumber(self, unit: _UNIT_WAVENUMBER) -> _T:
        raise NotImplementedError
