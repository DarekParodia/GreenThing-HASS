from homeassistant.helpers.entity_platform import async_add_entities
from .sensor import GreenThingSensor
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass, config_entry):
    """Set up GreenThing from a config entry."""
    # Example: Dynamically create multiple sensors
    sensors = [
        GreenThingSensor("sensor_1", "initial_state_1")
    ]

    # Add sensors to the platform
    async_add_entities = hass.data.get("sensor_platform_add_entities")
    if async_add_entities:
        async_add_entities(sensors)

    return True