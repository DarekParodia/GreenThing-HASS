"""Platform for light integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Green Thing lights."""
    lights = [
        GreenThingLight("Light 1", "light_1"),
        GreenThingLight("Light 2", "light_2"),
    ]
    async_add_entities(lights)

class GreenThingLight(LightEntity):
    """Representation of a Green Thing Light."""

    def __init__(self, name: str, unique_id: str) -> None:
        """Initialize a Green Thing light."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        self._attr_is_on = False
        self.async_write_ha_state()
