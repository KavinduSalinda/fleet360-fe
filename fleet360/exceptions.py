from rest_framework.views import exception_handler
from rest_framework import status
from fleet360.responses import StandardResponse


def custom_exception_handler(exc, context):
    """
    Returns exceptions in StandardResponse format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Get default status code or 500
        code = response.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR

        # Default DRF error messages
        if isinstance(response.data, dict):
            message = response.data.get("detail") or list(response.data.values())[0]
        else:
            message = str(response.data)

        return StandardResponse(data=None, message=message, code=code)

    # Fallback for unhandled exceptions
    return StandardResponse(
        data=None, message=str(exc), code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
