"API acccess exception classes."


class APIError(Exception):
    "Base exception class for API access errors."


class RecordDoesNotExist(APIError):
    "Base exception for accessing missing records."


class PatientDoesNotExist(APIError):
    "Patient record does not exist exception."


class ProviderDoesNotExist(APIError):
    "Provider record does not exist exception."