from homeassistant.helpers.entity import Entity

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
        self._state = "updated_state_value"