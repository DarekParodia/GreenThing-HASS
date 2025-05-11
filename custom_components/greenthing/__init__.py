"""The GreenThing integration."""
# from homeassistant.const import CONF_HOST, CONF_PORT
# from .sensor import GreenThingSensor

# async def async_setup_entry(hass, config_entry):
#     """Set up the GreenThing sensor from a config entry."""
#     host = config_entry.data[CONF_HOST]
#     port = config_entry.data[CONF_PORT]

#     # Example sensor data
#     sensors = [
#         GreenThingSensor("Temperature", "2"),
#         GreenThingSensor("Humidity", "3"),
#     ]
#     async_add_entities(sensors, True)
#     return True

# async def async_setup(hass, config):
#     """Set up the GreenThing component."""
#     # We allow config via YAML, but we don't use it.
#     return True