from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT

# Define the schema for the form
data_schema = {
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int
}
@config_entries.HANDLERS.register(DOMAIN)
class GreenThingConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for GreenThing."""

    VERSION = 1
    DOMAIN = "greenthing"

    def __init__(self):
        """Initialize the config flow."""
        self._host = None
        self._port = None

    async def async_step_import(self, user_input=None):
        """Handle import from YAML."""
        if user_input is None:
            return self.async_show_form(
                step_id="import", data_schema=vol.Schema(data_schema)
            )

        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            if not host:
                errors["base"] = "invalid_host"
            elif not (0 < port < 65536):
                errors["base"] = "invalid_port"
            else:
                return self.async_create_entry(
                    title=host,
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )
    
class GreenThingOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for GreenThing."""

    VERSION = 1
    DOMAIN = "greenthing"

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry
        self._host = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Validate the input
            self._host = str(user_input[CONF_HOST])
            self._port = user_input[CONF_PORT]

            if not self._host:
                errors["base"] = "invalid_host"
            elif not (0 < self._port < 65536):
                errors["base"] = "invalid_port"
            else:
                # If the input is valid, proceed to update the entry
                return self.async_create_entry(
                    title=DOMAIN,
                    data={
                        CONF_HOST: self._host,
                        CONF_PORT: self._port,
                    },
                )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )