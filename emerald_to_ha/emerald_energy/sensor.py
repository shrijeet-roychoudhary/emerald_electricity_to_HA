from datetime import timedelta, datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN
from .emerald_api_client import EmeraldApiClient

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    email = config_entry.data[CONF_EMAIL]
    password = config_entry.data[CONF_PASSWORD]
    
    api_client = EmeraldApiClient(email, password)
    
    properties = await hass.async_add_executor_job(api_client.get_properties)
    if not properties or "info" not in properties or not properties["info"]["property"]:
        _LOGGER.error("Could not find any properties for this account.")
        return

    device_id = properties["info"]["property"][0]["devices"][0]["id"]
    
    async_add_entities([EmeraldEnergySensor(api_client, device_id)])

class EmeraldEnergySensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, api_client, device_id):
        """Initialize the sensor."""
        self._api_client = api_client
        self._device_id = device_id
        self._state = None
        self._unit_of_measurement = "kWh"
        self._attr_unique_id = f"emerald_energy_{device_id}"

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

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return "energy"

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return "total_increasing"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        today = datetime.now().strftime("%Y-%m-%d")
        energy_data = await self.hass.async_add_executor_job(
            self._api_client.get_energy_data, self._device_id, today, today
        )

        if energy_data and "info" in energy_data and energy_data["info"]["daily_consumptions"]:
            total_kwh_of_day = energy_data["info"]["daily_consumptions"][0]["total_kwh_of_day"]
            try:
                self._state = float(total_kwh_of_day)
            except (ValueError, TypeError):
                self._state = None
        else:
            self._state = None
