import asyncio
from datetime import timedelta
import json
import logging

import requests

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import BASE_API_URL, FALLBACK_SUMMARY

_LOGGER = logging.getLogger(__name__)

SUMMARY_KEYS = ("numero1", "numero2", "numero3")


class ElGordoCoordinator(DataUpdateCoordinator):
    """Class to manage fetching El Gordo data."""

    def __init__(self, hass, entry):
        """Initialize."""
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name="El Gordo",
            update_interval=timedelta(minutes=30),
        )

    def _fetch_data(self, url):
        """Fetch data and strip any JavaScript-style prefixes to get pure JSON."""
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text = response.text

        start_index = text.find("{")
        if start_index == -1:
            raise ValueError("API response does not contain JSON")

        return json.loads(text[start_index:])

    @staticmethod
    def _has_current_summary(summary):
        """Return whether the API response contains a complete draw summary."""
        return isinstance(summary, dict) and all(
            summary.get(key) for key in SUMMARY_KEYS
        )

    async def _async_update_data(self):
        tickets_str = self.entry.options.get(
            "tickets", self.entry.data.get("tickets", "")
        )
        tickets = [t.strip() for t in tickets_str.split(",") if t.strip()]

        try:
            async with asyncio.timeout(15):
                results = {"tickets": {}, "summary": {}}

                summary_url = f"{BASE_API_URL}?n=resumen"
                summary = await self.hass.async_add_executor_job(
                    self._fetch_data, summary_url
                )

                if not self._has_current_summary(summary):
                    results["summary"] = FALLBACK_SUMMARY.copy()
                    return results

                results["summary"] = summary

                for ticket in tickets:
                    ticket_url = f"{BASE_API_URL}?n={ticket}"
                    ticket_data = await self.hass.async_add_executor_job(
                        self._fetch_data, ticket_url
                    )
                    if not isinstance(ticket_data, dict) or "premio" not in ticket_data:
                        raise ValueError(
                            f"API returned no prize data for ticket {ticket}"
                        )
                    results["tickets"][ticket] = ticket_data

                return results
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
