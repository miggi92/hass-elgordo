import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=60)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    ticket_number = entry.data["ticket_number"]
    async_add_entities([ElGordoSensor(ticket_number)], True)

class ElGordoSensor(SensorEntity):
    """Representation of an El Gordo sensor."""

    def __init__(self, ticket_number):
        self._ticket_number = ticket_number
        self._state = None
        self._attr_name = f"El Gordo Ticket {ticket_number}"
        self._attr_unique_id = f"elgordo_{ticket_number}"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        api_url = f"https://api.elpais.com/ws/LoteriaNavidadPremiados?n={self._ticket_number}"
        try:
            response = requests.get(api_url, timeout=10)
            # Remove the 'busqueda=' prefix from the API response
            clean_json = response.text.replace('busqueda=', '')
            import json
            data = json.loads(clean_json)
            self._state = data.get('premio', 0)
        except Exception:
            self._state = None