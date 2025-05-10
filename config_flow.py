from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class GreenThingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GreenThing."""

    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Define the schema for the form
        data_schema = {
            vol.Required("host"): str,
            vol.Optional("port", default=80): int,
        }

        if user_input is not None:
            # Validate the input
            self._host = str(user_input["host"])
            self._port = int(user_input["port"])

            if not self._host:
                errors["base"] = "invalid_host"
            elif not (0 < self._port < 65536):
                errors["base"] = "invalid_port"
            else:
                # If the input is valid, proceed to create the entry
                return self.async_create_entry(
                    title=self._host,
                    data={
                        "host": self._host,
                        "port": self._port,
                    },
                )
        
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )