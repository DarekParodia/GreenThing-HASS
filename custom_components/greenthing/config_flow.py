from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT

# Define the schema for the form
data_schema = {
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
}
class GreenThingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GreenThing."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the input
            self._host = str(user_input[CONF_HOST])
            self._port = int(user_input[CONF_PORT])

            if not self._host:
                errors["base"] = "invalid_host"
            elif not (0 < self._port < 65536):
                errors["base"] = "invalid_port"
            else:
                # If the input is valid, proceed to create the entry
                return self.async_create_entry(
                    title=self._host,
                    data={
                        CONF_HOST: self._host,
                        CONF_PORT: self._port,
                    },
                )
        
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
    
class GreenThingOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for GreenThing."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry
        self._host = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Validate the input
            self._host = str(user_input[CONF_HOST])
            self._port = int(user_input[CONF_PORT])

            if not self._host:
                errors["base"] = "invalid_host"
            elif not (0 < self._port < 65536):
                errors["base"] = "invalid_port"
            else:
                # If the input is valid, proceed to update the entry
                return self.async_create_entry(
                    title=self._host,
                    data={
                        CONF_HOST: self._host,
                        CONF_PORT: self._port,
                    },
                )

        return self.async_show_form(
            step_id="init", data_schema=data_schema, errors=errors
        )