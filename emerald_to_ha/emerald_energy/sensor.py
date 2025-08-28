from datetime import timedelta, datetime
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN
from .emerald_api_client import EmeraldApiClient

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=60)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    email = config_entry.data[CONF_EMAIL]
    password = config_entry.data[CONF_PASSWORD]
    
    api_client = EmeraldApiClient(email, password)
    
    properties = await hass.async_add_executor_job(api_client.get_properties)
    if not properties or "info" not in properties or not properties["info"]["property"]:
        _LOGGER.error("Could not find any properties for this account.")
        return

    device_id = properties["info"]["property"][0]["devices"]["id"]
    
    async_add_entities([EmeraldEnergySensor(api_client, device_id)])

class EmeraldEnergySensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, api_client, device_id):
        """Initialize the sensor."""
        self._api_client = api_client
        self._device_id = device_id
        self._state = None
        self._unit_of_measurement = "kWh"

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Emerald Energy'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    async def async_update(self):
        """Fetch new state data for the sensor."""
        today = datetime.now().strftime("%Y-%m-%d")
        energy_data = await self.hass.async_add_executor_job(
            self._api_client.get_energy_data, self._device_id, today, today
        )

        if energy_data and "daily_consumptions" in energy_data:
            daily_consumption = energy_data["daily_consumptions"][0]
            self._state = daily_consumption["total"]
        else:
            self._state = None
