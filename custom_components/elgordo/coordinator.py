from datetime import timedelta
import logging
import asyncio
import requests
import json

from .const import DOMAIN, BASE_API_URL
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class ElGordoCoordinator(DataUpdateCoordinator):
    """Class to manage fetching El Gordo data."""

    def __init__(self, hass, ticket_number):
        """Initialize."""
        self.ticket_number = ticket_number
        super().__init__(
            hass,
            _LOGGER,
            name="El Gordo",
            update_interval=timedelta(minutes=30),
        )

    def _fetch_data(self, url):
        """Helper to fetch and clean JSON data."""
        response = requests.get(url, timeout=10)
        # Clean the 'busqueda=' prefix
        content = response.text.replace('busqueda=', '')
        return json.loads(content)

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with asyncio.timeout(15):
                # Fetch ticket specific data
                ticket_url = f"{BASE_API_URL}?n={self.ticket_number}"
                summary_url = f"{BASE_API_URL}?n=resumen"
                
                ticket_data = await self.hass.async_add_executor_job(self._fetch_data, ticket_url)
                summary_data = await self.hass.async_add_executor_job(self._fetch_data, summary_url)

                return {
                    "ticket": ticket_data,
                    "summary": summary_data
                }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")