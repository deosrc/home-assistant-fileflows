
from dateutil import parser

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, DATA_BYTES, DATA_GIGABYTES
from homeassistant.components.sensor.const import SensorDeviceClass

from .coordinator import NodeInfoDataUpdateCoordinator, RunnerInfoDataUpdateCoordinator
from .const import DOMAIN
from .entity import RunnerEntity

async def async_setup_entry(hass, entry, async_add_devices):
    # TODO: Work out how to add new nodes/runners as they appear

    # Get number of runners per node
    node_info_coordinator = hass.data[DOMAIN][entry.entry_id][NodeInfoDataUpdateCoordinator]
    node_info = [{"id": d.get("Uid"), "name": d.get("Name"), "runner_count": d.get("FlowRunners")} for d in node_info_coordinator.data]

    runner_info_coordinator = hass.data[DOMAIN][entry.entry_id][RunnerInfoDataUpdateCoordinator]

    for ni in node_info:
        for runner_idx in range(ni["runner_count"]):
            async_add_devices([
                StartedRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                CurrentPartRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                CurrentPartProgressRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                FileLibraryRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                FilePathRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                FileOriginalSizeRunnerSensor(runner_info_coordinator, entry, ni, runner_idx),
                FlowRunnerSensor(runner_info_coordinator, entry, ni, runner_idx)
            ])


class StartedRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Started"
    _attr_icon = "mdi:clock"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_started"

    @property
    def native_value(self):
        value = self._data.get("StartedAt")
        return parser.parse(value) if value else None


class CurrentPartRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Current Part"

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_current_part"

    @property
    def native_value(self):
        return self._data.get("CurrentPartName")

    @property
    def extra_state_attributes(self):
        return super().extra_state_attributes | {
            "Part Number": self._data.get("CurrentPart"),
            "Total Parts": self._data.get("TotalParts"),
        }


class CurrentPartProgressRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Current Part Progress"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_suggested_display_precision = 1

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_current_part_progress"

    @property
    def native_value(self):
        return self._data.get("CurrentPartPercent")


class FileLibraryRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Library"

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_file_library"

    @property
    def native_value(self):
        return self._data.get("Library", {}).get("Name")


class FilePathRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "File Path"

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_file_path"

    @property
    def native_value(self):
        return self._data.get("LibraryFile", {}).get("RelativePath")


class FileOriginalSizeRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Original File Size"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = DATA_BYTES
    _attr_suggested_unit_of_measurement = DATA_GIGABYTES
    _attr_suggested_display_precision = 2

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_file_original_size"

    @property
    def native_value(self):
        return self._data.get("LibraryFile", {}).get("OriginalSize")


class FlowRunnerSensor(RunnerEntity, SensorEntity):

    _attr_has_entity_name = True
    _attr_name = "Flow"

    @property
    def unique_id(self):
        return f"{self._unique_id_prefix}_flow"

    @property
    def native_value(self):
        return self._data.get("LibraryFile", {}).get("FlowName")
