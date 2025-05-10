import requests
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from .const import DOMAIN, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the GreenThing sensor from a config entry."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]

    # Example sensor data
    sensors = [
        GreenThingSensor("Temperature", "2"),
        GreenThingSensor("Humidity", "3"),
    ]
    async_add_entities(sensors, True)

class GreenThingSensor(Entity):
    """Representation of a GreenThing sensor."""

    def __init__(self, name, state):
        """Initialize the sensor."""
        self._name = name
        self._state = state

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"greenthing_{self._name.lower()}"
    
    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Update the state here (e.g., fetch data from an API)
        self._state = await self._fetch_sensor_data()
    
    async def _fetch_sensor_data(self):
        return 25.0