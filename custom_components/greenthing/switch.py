"""Platform for switch integration."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GreenThing switch."""
    switches = [
        GreenThingSwitch("Main Switch", "main_switch"),
    ]
    async_add_entities(switches)

class GreenThingSwitch(SwitchEntity):
    """Representation of a GreenThing switch."""

    def __init__(self, name: str, unique_id: str) -> None:
        """Initialize the switch."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{unique_id}"
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
        self.async_write_ha_state()
