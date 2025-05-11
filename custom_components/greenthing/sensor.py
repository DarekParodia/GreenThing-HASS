import requests
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([Button()])

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

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Update the state here (e.g., fetch data from an API)
        self._state = await self._fetch_sensor_data()
    
    async def _fetch_sensor_data(self):
        return 25.0
    
class Button(SwitchEntity):
    """Representation of a GreenThing button."""
    _attr_has_entity_name = True
    _attr_name = "GreenThing Button"

    def __init__(self):
        self._is_on = False
        self._attr_device_info = ...  # For automatic device registration
        self._attr_unique_id = ...

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False