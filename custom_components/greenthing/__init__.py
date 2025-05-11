"""The Green Thing integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import ConfigEntryNotReady

import aiohttp

from .switch import GreenThingSwitch

DOMAIN = "greenthing"

async def get_datapoints(api_url: str) -> list:
    """Fetch the list of datapoints from the API."""
    async with aiohttp.ClientSession() as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["datapoints"]
                    else:
                        raise ConfigEntryNotReady(f"Error fetching datapoints: {response.status}")
        except aiohttp.ClientError as e:
            raise ConfigEntryNotReady(f"Error connecting to API: {e}")

async def get_sensors(api_url: str) -> list:
    """Convert datapoints to homeassistant sensors."""
    datapoints = await get_datapoints(api_url)
    sensors = []
    for dp in datapoints:
        match dp["type"]:
            case 1:
                # Solenoid class not implemented yet
                pass
            case 2:
                # Button
                sensors.append(GreenThingSwitch(dp["name"]))
            case _:
                continue
    return sensors



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up Green Thing from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["light", "switch"])

    api_url = f"http://{entry.data['host']}:{entry.data['port']}/"

    try:
        sensors = await get_sensors(api_url)
    except ConfigEntryNotReady as e:
        raise ConfigEntryNotReady(f"Error setting up Green Thing: {e}")
    if not sensors:
        raise ConfigEntryNotReady("No sensors found")

    # Add the sensors to the entity registry
    async_add_entities(sensors, True)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["light", "switch"])
