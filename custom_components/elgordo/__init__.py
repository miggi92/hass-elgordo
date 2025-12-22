from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import ElGordoCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up El Gordo from a config entry."""
    # Use 'number' from your config_flow
    coordinator = ElGordoCoordinator(hass, entry.data["number"])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Wenn kein Ticket-Eintrag mehr existiert, Flag für globale Sensoren zurücksetzen
        remaining_entries = [e for e in hass.data[DOMAIN] if e != "global_sensors_created"]
        if not remaining_entries:
            hass.data[DOMAIN]["global_sensors_created"] = False
            
    return unload_ok