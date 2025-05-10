import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entry_id = config_entry.entry_id
    data = hass.data["greenthing"][entry_id]
    host = data["host"]
    port = data["port"]
    fetch_sensor_data = data["fetch_sensor_data"]

    sensors = [
        GreenThingSensor(hass, host, port, "Temperature", fetch_sensor_data),
        GreenThingSensor(hass, host, port, "Humidity", fetch_sensor_data),
    ]
    async_add_entities(sensors, True)


class GreenThingSensor(Entity):
    """Representation of a GreenThing sensor."""

    def __init__(self, hass, host, port, name, fetch_sensor_data):
        """Initialize the sensor."""
        self._hass = hass
        self._host = host
        self._port = port
        self._name = name
        self._state = None  # Initialize state to None
        self._fetch_sensor_data = fetch_sensor_data # Store the data fetching function

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"GreenThing {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"greenthing_{self._name.lower()}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            self._state = await self._fetch_sensor_data(self._name.lower())
        except Exception as e:
            _LOGGER.error(f"Error updating sensor {self._name}: {e}")
            self._state = None