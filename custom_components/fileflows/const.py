NAME = "FileFlows"
DOMAIN = "fileflows"

PLATFORMS = ["sensor", "binary_sensor", "number", "switch", "update"]

STATUS_MAP = {
    # Copy of enum from https://github.com/revenz/FileFlows/blob/master/Shared/Models/LibraryFile.cs
    # Required since API only returns non-zero counts
    -3: "On Hold",
    -2: "Disabled",
    -1: "Out of Schedule",
    0: "Unprocessed",
    1: "Processed",
    2: "Processing",
    3: "Flow Not Found",
    4: "Failed",
    5: "Duplicate",
    6: "Mapping Issue",
    7: "Missing Library"
}
