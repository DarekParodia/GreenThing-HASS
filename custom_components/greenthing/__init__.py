"""The GreenThing integration."""
from homeassistant.const import CONF_HOST, CONF_PORT
from .sensor import GreenThingSensor
import asyncio

async def async_setup_entry(hass, config_entry):
    """Set up the GreenThing sensor from a config entry."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]

    # Define a function to fetch sensor data (replace with your actual data fetching logic)
    async def fetch_sensor_data(sensor_type):
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

    # Create sensor entities
    sensors = [
        GreenThingSensor(hass, host, port, "Temperature", fetch_sensor_data),
        GreenThingSensor(hass, host, port, "Humidity", fetch_sensor_data),
    ]

    async_add_entities = hass.helpers.entity_platform.async_get_current_platform().async_add_entities
    async_add_entities(sensors, True)

    return True


async def async_setup(hass, config):
    """Set up the GreenThing component."""
    # We allow config via YAML, but we don't use it.
    return True