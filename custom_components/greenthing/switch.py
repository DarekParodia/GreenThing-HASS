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
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_HOST, CONF_PORT, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GreenThing switches from API response."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    api_url = f"http://{host}:{port}/"

    # Get existing entity IDs to prevent duplicates
    existing_entities = hass.states.async_entity_ids("switch")
    existing_greenthing_switches = {
        entity_id.split('.')[1] for entity_id in existing_entities 
        if entity_id.startswith(f"switch.{DOMAIN}_")
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        switches = []
                        for point in data["dataPoints"]:
                            if point["type"] == 2:  # Type 2 is for buttons
                                # Create unique_id for comparison
                                unique_id = f"{DOMAIN}_{point['name'].lower()}"
                                
                                # Only add if switch doesn't already exist
                                if unique_id not in existing_greenthing_switches:
                                    switches.append(
                                        GreenThingSwitch(
                                            name=point["name"],
                                            api_url=f"http://{host}:{port}/",
                                            initial_state=point["state"]
                                        )
                                    )
                                else:
                                    _LOGGER.debug(
                                        "Switch %s already exists, skipping", 
                                        point["name"]
                                    )
                                    
                        if switches:
                            async_add_entities(switches)
                        else:
                            _LOGGER.info("No new switches to add")
                    else:
                        _LOGGER.error("Failed to fetch switches from API: %s", response.status)
                        raise ConfigEntryNotReady
        except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
            _LOGGER.error("Error connecting to GreenThing API: %s", err)
            raise ConfigEntryNotReady

class GreenThingSwitch(SwitchEntity):
    """Representation of a GreenThing switch."""

    # should_poll = True
    # scan_interval = SCAN_INTERVAL

    def __init__(self, name: str, api_url: str, initial_state: bool) -> None:
        """Initialize the switch."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{name.lower()}"
        self._is_on = initial_state
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
                    async with session.get(self._api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            for point in data["dataPoints"]:
                                if point["name"] == self._attr_name:
                                    self._is_on = point["state"]
                                    self.async_write_ha_state()
                                    break
            except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
                _LOGGER.error("Error updating switch state: %s", err)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # payload = {
        #     "name": self._attr_name,
        #     "state": True
        # }
        # async with aiohttp.ClientSession() as session:
        #     try:
        #         async with session.post(
        #             self._api_url,
        #             data=json.dumps(payload),
        #             headers={"Content-Type": "application/json"}
        #         ) as response:
        #             if response.status == 200:
        #                 self._is_on = True
        #                 self.async_write_ha_state()
        #     except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
        #         _LOGGER.error("Error turning switch on: %s", err)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # payload = {
        #     "name": self._attr_name,
        #     "state": False
        # }
        # async with aiohttp.ClientSession() as session:
        #     try:
        #         async with session.post(
        #             self._api_url,
        #             data=json.dumps(payload),
        #             headers={"Content-Type": "application/json"}
        #         ) as response:
        #             if response.status == 200):
        #                 self._is_on = False
        #                 self.async_write_ha_state()
        #     except (aiohttp.ClientError, async_timeout.TimeoutError) as err:
        #         _LOGGER.error("Error turning switch off: %s", err)

    async def async_update(self) -> None:
        """Update switch state."""
        await self._update_state()
