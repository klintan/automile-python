class AutomileAPIError(Exception):
    "Base class for errors from the Billogram API"

    def __init__(self, message, **kwargs):
        super(AutomileException, self).__init__(message)

        self.field = kwargs.get('field', None)
        self.field_path = kwargs.get('field_path', None)

        self.extra_data = kwargs
        if 'field' in self.extra_data:
            del self.extra_data['field']
        if 'field_path' in self.extra_data:
            del self.extra_data['field_path']
        if not self.extra_data:
            self.extra_data = None

class ServiceMalfunctioningError(AutomileAPIError):
    "The Billogram API service seems to be malfunctioning"
    pass


class RequestFormError(AutomileAPIError):
    "Errors caused by malformed requests"
    pass


class PermissionDeniedError(AutomileAPIError):
    "No permission to perform the requested operation"
    pass


class InvalidAuthenticationError(PermissionDeniedError):
    "The user/key combination could not be authenticated"
    pass


class NotAuthorizedError(PermissionDeniedError):
    "The user does not have authorization to perform the requested operation"
    pass


class RequestDataError(AutomileAPIError):
    "Errors caused by bad data passed to request"
    pass


class UnknownFieldError(RequestDataError):
    "An unknown field was passed in the request data"
    pass


class MissingFieldError(RequestDataError):
    "A required field was missing from the request data"
    pass


class InvalidFieldCombinationError(RequestDataError):
    "Mutually exclusive fields were specified together"
    pass


class InvalidFieldValueError(RequestDataError):
    "A field was given an out-of-range value or a value of incorrect type"
    pass


class ReadOnlyFieldError(RequestDataError):
    "Attempt to modify a read-only field"
    pass


class InvalidObjectStateError(RequestDataError):
    "The request can not be performed on an object in this state"
    pass


class ObjectNotFoundError(RequestDataError):
    "No object by the requested ID exists"
    pass


class ObjectNotAvailableYetError(ObjectNotFoundError):
    "No object by the requested ID exists, but is expected to be created soon"
    pass
