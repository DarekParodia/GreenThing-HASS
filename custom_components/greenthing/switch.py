"""Platform for switch integration."""
from __future__ import annotations
import aiohttp
import async_timeout
import logging
import json
from typing import Any

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, CONF_HOST, CONF_PORT, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class GreenThingSwitch(SwitchEntity):
    """Representation of a GreenThing switch."""

    # should_poll = True
    # scan_interval = SCAN_INTERVAL

    def __init__(self, name: str) -> None:
        """Initialize the switch."""


    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def _update_state(self) -> None:
        """Fetch switch state from API."""


    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""


    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""

    async def async_update(self) -> None:
        """Update switch state."""
        await self._update_state()
