import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ElGordoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for El Gordo."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"Ticket {user_input['ticket_number']}", 
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ticket_number"): str,
            }),
        )