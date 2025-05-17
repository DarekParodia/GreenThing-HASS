"""Platform for switch integration."""
from __future__ import annotations
import aiohttp
import async_timeout
import logging
import json
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN
from .api import ApiHandler

_LOGGER = logging.getLogger(__name__)
API_URL = None
API_HANDLER = None

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the switch platform."""
    API_URL = hass.data[DOMAIN][entry.entry_id]["api_url"]
    API_HANDLER = ApiHandler(API_URL)

    switches = [] 
    for datapoint in API_HANDLER.get_datapoints():
        if datapoint["type"] == 2:
            switches.append(GreenThingSwitch(datapoint["name"], datapoint["state"]))
    async_add_entities(switches, True)
class GreenThingSwitch(SwitchEntity):
    """Representation of a GreenThing switch."""

    def __init__(self, name: str, initial_state: bool) -> None:
        """Initialize the switch."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{name.lower()}"
        self._is_on = initial_state

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def _update_state(self) -> None:
        """Fetch switch state from API."""
        state = await API_HANDLER.getState(self._attr_name)
        if state is not None:
            self._is_on = state
            self._attr_is_on = self._is_on
        else:
            _LOGGER.error("Failed to fetch state for %s", self._attr_name)


    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""


    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""

    async def async_update(self) -> None:
        """Update switch state."""
        await self._update_state()
