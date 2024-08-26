import itertools
import math
from typing import Final

import pytest

from spectral_unit_convert import Frequency, Wavelength, Wavenumber

FREQUENCY_MEASURES: Final = (Frequency, Wavelength, Wavenumber)


@pytest.mark.parametrize(
    "src_measure", FREQUENCY_MEASURES, ids=lambda m: f"src={m.__name__}"
)
@pytest.mark.parametrize(
    "dst_measure", FREQUENCY_MEASURES, ids=lambda m: f"dst={m.__name__}"
)
def test_frequency_measure_conversion_roundtrips(src_measure, dst_measure) -> None:
    """
    Verify that, for frequency measures A and B, the conversion A->B->A produces
    the original frequency measure.
    """
    value = 1234.0

    for src_unit, dst_unit in itertools.product(
        src_measure._SCALES.keys(), dst_measure._SCALES.keys()
    ):
        original = src_measure(value, src_unit)
        round_trip = original.as_unit(dst_measure, dst_unit).as_unit(
            src_measure, src_unit
        )
        assert math.isclose(original.value, round_trip.value)
        assert original.scale == round_trip.scale


@pytest.mark.parametrize(
    "src_measure", FREQUENCY_MEASURES, ids=lambda m: f"src={m.__name__}"
)
@pytest.mark.parametrize(
    "int_measure", FREQUENCY_MEASURES, ids=lambda m: f"int={m.__name__}"
)
@pytest.mark.parametrize(
    "dst_measure", FREQUENCY_MEASURES, ids=lambda m: f"dst={m.__name__}"
)
def test_frequency_measure_conversion_path_independent(
    src_measure, int_measure, dst_measure
) -> None:
    """
    Verify that, for frequency measures A,B,C, the conversion A->B->C produces
    the same frequency measure as the conversion A->C.
    """
    value = 1234.0

    for src_unit, int_unit, dst_unit in itertools.product(
        src_measure._SCALES.keys(),
        int_measure._SCALES.keys(),
        dst_measure._SCALES.keys(),
    ):
        original = src_measure(value, src_unit)

        direct = original.as_unit(dst_measure, dst_unit)

        indirect = original.as_unit(int_measure, int_unit).as_unit(
            dst_measure, dst_unit
        )

        assert math.isclose(direct.value, indirect.value)
        assert direct.scale == indirect.scale
