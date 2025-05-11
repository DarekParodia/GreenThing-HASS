"""Platform for switch integration."""
from __future__ import annotations
import aiohttp
import async_timeout
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GreenThing switches from API response."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    api_url = f"http://{host}:{port}/"  # Adjust the endpoint as needed

    async with aiohttp.ClientSession() as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        switches = []
                        for switch_data in data["dataPoints"]:  # Adjust based on your API response structure
                            if switch_data["type"] == 2:
                                switches.append(
                                    GreenThingSwitch(
                                        name=switch_data["name"],
                                        api_url=f"http://{host}:{port}/"
                                    )
                                )
                        async_add_entities(switches)
                    else:
                        _LOGGER.error("Failed to fetch switches from API: %s", response.status)
                        raise ConfigEntryNotReady
        except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
            _LOGGER.error("Error connecting to GreenThing API: %s", err)
            raise ConfigEntryNotReady
        
def get_switch_from_name(name: str, json_data: dict) -> dict:
    """Get switch data from name."""
    for switch in json_data["dataPoints"]:
        if switch["name"] == name:
            return switch
    return {}

class GreenThingSwitch(SwitchEntity):
    """Representation of a GreenThing switch."""

    def __init__(self, name: str, api_url: str) -> None:
        """Initialize the switch."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{name.lower()}"
        self._is_on = False
        self._api_url = api_url

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def _update_state(self) -> None:
        """Fetch switch state from API."""
        async with aiohttp.ClientSession() as session:
            try:
                async with async_timeout.timeout(10):
                    async with session.get(f"{self._api_url}/") as response:
                        if response.status == 200:
                            data = await response.json()
                            switch_data = get_switch_from_name(self._attr_name, data)
                            if switch_data:
                                self._is_on = switch_data["state"] == "true"
                                self.async_write_ha_state()
            except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
                _LOGGER.error("Error updating switch state: %s", err)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # async with aiohttp.ClientSession() as session:
        #     try:
        #         async with session.post(f"{self._api_url}/on") as response:
        #             if response.status == 200:
        #                 self._is_on = True
        #                 self.async_write_ha_state()
        #     except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
        #         _LOGGER.error("Error turning switch on: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # async with aiohttp.ClientSession() as session:
        #     try:
        #         async with session.post(f"{self._api_url}/off") as response:
        #             if response.status == 200:
        #                 self._is_on = False
        #                 self.async_write_ha_state()
        #     except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
        #         _LOGGER.error("Error turning switch off: %s", err)

    async def async_update(self) -> None:
        """Update switch state."""
        await self._update_state()
