from enum import Enum


class ConfigName(Enum):
    CLOUD = "cloud"
    DATABASE = "database"
    PLC = "plc"


class ErrorType(Enum):
    INVALID_TYPE = "Invalid type"
    MISSING_VALUE = "Missing value"
    OUT_OF_RANGE = "Out of range"
