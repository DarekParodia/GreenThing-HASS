import aiohttp
import async_timeout
from homeassistant.exceptions import ConfigEntryNotReady

class ApiHandler:
    """Handle the API requests."""

    def __init__(self, api_url):
        """Initialize the API handler."""
        self.api_url = api_url


    async def getDatapoint(self, datapoint_name: str):
        """Get the state of a datapoint."""
        async with aiohttp.ClientSession() as session:
            try:
                async with async_timeout.timeout(10):
                    async with session.get(self.api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            datapoints = data["dataPoints"] 
                            for datapoint in datapoints:
                                if datapoint["name"] == datapoint_name:
                                    return datapoint
                            return None
                        else:
                            raise ConfigEntryNotReady(f"Error fetching datapoints: {response.status}")
            except aiohttp.ClientError as e:
                raise ConfigEntryNotReady(f"Error connecting to API: {e}")
            
    async def getState(self, datapoint_name: str):
        datapoint = await self.getDatapoint(datapoint_name)
        if datapoint:
            return datapoint["state"]
        return None