"""Constants for the GreenThing integration."""
from datetime import timedelta

DOMAIN = "greenthing"

# Configuration keys
CONF_HOST = "host"
CONF_PORT = "port"

# Default values
DEFAULT_PORT = 80

# Scan interval needs to be a timedelta object
SCAN_INTERVAL = timedelta(seconds=1)