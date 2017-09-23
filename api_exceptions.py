class AutomileException(Exception):
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

class PermissionDeniedError(AutomileException):
    "No permission to perform the requested operation"
    pass
