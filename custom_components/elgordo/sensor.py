from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_TICKET_TYPE,
    DOMAIN,
    MANUFACTURER,
    TICKET_TYPE_DECIMO,
    prize_for_ticket_type,
)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    tickets_str = entry.options.get("tickets", entry.data.get("tickets", ""))
    tickets = [t.strip() for t in tickets_str.split(",") if t.strip()]
    ticket_type = entry.options.get(
        "ticket_type", entry.data.get("ticket_type", DEFAULT_TICKET_TYPE)
    )

    entities = []
    # Individual Ticket Sensors
    for ticket in tickets:
        entities.append(TicketPrizeSensor(coordinator, ticket, ticket_type))

    # Global Prize Sensors
    entities.extend(
        [
            MainPrizeSensor(coordinator, "first_prize", "numero1", "El Gordo"),
            MainPrizeSensor(coordinator, "second_prize", "numero2", "Second Prize"),
            MainPrizeSensor(coordinator, "third_prize", "numero3", "Third Prize"),
            MainPrizeSensor(
                coordinator, "fourth_prize_1", "numero4", "Fourth Prize 1"
            ),
            MainPrizeSensor(
                coordinator, "fourth_prize_2", "numero5", "Fourth Prize 2"
            ),
        ]
    )

    async_add_entities(entities)


class ElGordoBaseSensor(CoordinatorEntity, SensorEntity):
    """Base sensor with shared Device Info."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.entry.entry_id)},
            "name": "El Gordo Lottery",
            "manufacturer": MANUFACTURER,
            "model": "Spain Christmas Lottery",
        }


class TicketPrizeSensor(ElGordoBaseSensor):
    """Sensor for a specific ticket."""

    def __init__(self, coordinator, ticket, ticket_type):
        super().__init__(coordinator)
        self.ticket = ticket
        self.ticket_type = ticket_type
        self._attr_name = f"Ticket {ticket} Prize"
        self._attr_unique_id = f"{DOMAIN}_prize_{ticket}"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        ticket_data = self.coordinator.data["tickets"].get(self.ticket, {})
        return prize_for_ticket_type(ticket_data.get("premio"), self.ticket_type)

    @property
    def extra_state_attributes(self):
        return {
            "ticket_type": self.ticket_type,
            "ticket_type_name": (
                "Décimo" if self.ticket_type == TICKET_TYPE_DECIMO else "Billete"
            ),
        }

    @property
    def available(self):
        return super().available and self.ticket in self.coordinator.data["tickets"]

    @property
    def icon(self):
        return (
            "mdi:ticket-confirmation"
            if (self.native_value or 0) > 0
            else "mdi:ticket-outline"
        )


class MainPrizeSensor(ElGordoBaseSensor):
    """Sensor for general winning numbers."""

    def __init__(self, coordinator, key, api_key, label):
        super().__init__(coordinator)
        self._api_key = api_key
        self._attr_name = f"Winning Number {label}"
        self._attr_unique_id = f"{DOMAIN}_winning_{key}"

    @property
    def native_value(self):
        return self.coordinator.data["summary"].get(self._api_key)

    @property
    def extra_state_attributes(self):
        summary = self.coordinator.data["summary"]
        if "draw_year" not in summary:
            return None
        return {
            "data_source": summary["data_source"],
            "draw_year": summary["draw_year"],
        }

    @property
    def icon(self):
        return "mdi:trophy-variant"
