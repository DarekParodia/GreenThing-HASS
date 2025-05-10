"""The GreenThing integration."""
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .sensor import GreenThingSensor
import asyncio

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the GreenThing sensor from a config entry."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]

    # Define a function to fetch sensor data (replace with your actual data fetching logic)
    async def fetch_sensor_data(sensor_type: str):
        # Simulate fetching data from your GreenThing device
        # In a real implementation, you would use 'host' and 'port' to connect
        # to your device and retrieve the sensor value.
        await asyncio.sleep(1)  # Simulate network delay
        if sensor_type == "temperature":
            return 22.5  # Example temperature value
        elif sensor_type == "humidity":
            return 60.2  # Example humidity value
        else:
            return None

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )

    hass.data.setdefault("greenthing", {})[config_entry.entry_id] = {
        "host": host,
        "port": port,
        "fetch_sensor_data": fetch_sensor_data,
    }

    return True


async def async_setup(hass, config):
    """Set up the GreenThing component."""
    # We allow config via YAML, but we don't use it.
    return True