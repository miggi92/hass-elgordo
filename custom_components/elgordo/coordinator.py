import asyncio
import logging
import json
import requests
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, BASE_API_URL

_LOGGER = logging.getLogger(__name__)

class ElGordoCoordinator(DataUpdateCoordinator):
    """Class to manage fetching El Gordo data."""

    def __init__(self, hass, entry):
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )

    def _fetch_data(self, url):
        """Fetch and clean JSON data."""
        response = requests.get(url, timeout=10)
        content = response.text.replace('busqueda=', '')
        return json.loads(content)

    async def _async_update_data(self):
        """Fetch data from API."""
        tickets_str = self.entry.options.get("tickets", self.entry.data.get("tickets", ""))
        tickets = [t.strip() for t in tickets_str.split(",") if t.strip()]
        
        try:
            async with asyncio.timeout(30):
                results = {"tickets": {}, "summary": {}}
                # Global summary
                results["summary"] = await self.hass.async_add_executor_job(
                    self._fetch_data, f"{BASE_API_URL}?n=resumen"
                )
                # Individual tickets
                for ticket in tickets:
                    results["tickets"][ticket] = await self.hass.async_add_executor_job(
                        self._fetch_data, f"{BASE_API_URL}?n={ticket}"
                    )
                return results
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")