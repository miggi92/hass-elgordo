from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [TicketPrizeSensor(coordinator)]
    
    if not hass.data[DOMAIN].get("global_sensors_created"):
        entities.extend([
            MainPrizeSensor(coordinator, "first_prize", "numero1", "El Gordo"),
            MainPrizeSensor(coordinator, "second_prize", "numero2", "Second Prize"),
            MainPrizeSensor(coordinator, "third_prize", "numero3", "Third Prize"),
        ])
        hass.data[DOMAIN]["global_sensors_created"] = True
    
    async_add_entities(entities)

class ElGordoBaseSensor(SensorEntity):
    """Base class for El Gordo sensors."""
    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    @property
    def should_poll(self):
        return False

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))

class TicketPrizeSensor(ElGordoBaseSensor):
    """Sensor for the user's specific ticket prize."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = f"Prize Ticket {coordinator.ticket_number}"
        self._attr_unique_id = f"{DOMAIN}_prize_{coordinator.ticket_number}"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        return self.coordinator.data["ticket"].get("premio", 0)

    @property
    def icon(self):
        return "mdi:ticket-confirmation" if self.native_value > 0 else "mdi:ticket-outline"

class MainPrizeSensor(ElGordoBaseSensor):
    """Sensor for general winning numbers (Gordo, 2nd, 3rd)."""
    def __init__(self, coordinator, key, api_key, label):
        super().__init__(coordinator)
        self._api_key = api_key
        self._attr_name = f"Winning Number {label}"
        self._attr_unique_id = f"{DOMAIN}_winning_{key}"

    @property
    def native_value(self):
        return self.coordinator.data["summary"].get(self._api_key)
    
    @property
    def icon(self):
        return "mdi:trophy-variant"