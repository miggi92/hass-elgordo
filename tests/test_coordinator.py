import asyncio
from types import SimpleNamespace

import pytest

from custom_components.elgordo.const import (
    INITIAL_FALLBACK_SUMMARY,
    TICKET_TYPE_BILLETE,
    TICKET_TYPE_DECIMO,
    normalize_ticket_number,
    prize_for_ticket_type,
)
from custom_components.elgordo.coordinator import ElGordoCoordinator, SUMMARY_KEYS


class FakeHass:
    async def async_add_executor_job(self, _target, _url):
        return {"error": 1}


def test_verified_ticket_is_available_during_2025_fallback():
    coordinator = ElGordoCoordinator.__new__(ElGordoCoordinator)
    coordinator.entry = SimpleNamespace(
        options={}, data={"tickets": "27133,12345"}
    )
    coordinator.hass = FakeHass()
    coordinator._fallback_summary = INITIAL_FALLBACK_SUMMARY.copy()

    result = asyncio.run(coordinator._async_update_data())

    assert result["tickets"] == {"27133": {"premio": 0}}


def test_summary_requires_all_thirteen_drawn_prize_numbers():
    complete_summary = {
        key: str(index) for index, key in enumerate(SUMMARY_KEYS, start=1)
    }

    assert ElGordoCoordinator._has_current_summary(complete_summary)
    assert not ElGordoCoordinator._has_current_summary(
        {key: complete_summary[key] for key in SUMMARY_KEYS[:-1]}
    )


def test_fallback_contains_all_2025_fifth_prizes():
    assert [INITIAL_FALLBACK_SUMMARY[key] for key in SUMMARY_KEYS[5:]] == [
        "23112",
        "60649",
        "77715",
        "25412",
        "61366",
        "94273",
        "41716",
        "18669",
    ]


def test_prize_is_converted_from_billete_to_configured_ticket_type():
    assert prize_for_ticket_type(4_000_000, TICKET_TYPE_BILLETE) == 4_000_000
    assert prize_for_ticket_type(4_000_000, TICKET_TYPE_DECIMO) == 400_000
    assert prize_for_ticket_type(1_000, TICKET_TYPE_DECIMO) == 100

    with pytest.raises(ValueError, match="Unsupported ticket type"):
        prize_for_ticket_type(1_000, "unknown")


def test_ticket_number_is_normalized_to_five_digits():
    assert normalize_ticket_number(5490) == "05490"
    assert normalize_ticket_number("05490") == "05490"
    assert normalize_ticket_number(None) is None
