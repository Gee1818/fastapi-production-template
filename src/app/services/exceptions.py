from dataclasses import dataclass


@dataclass
class DataValidationError(Exception):
    message: str
