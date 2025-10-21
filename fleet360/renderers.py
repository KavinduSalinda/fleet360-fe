from rest_framework.renderers import JSONRenderer
from rest_framework import status
from fleet360.responses import StandardResponse


class StandardResponseRenderer(JSONRenderer):
    """
    Custom renderer that automatically wraps all responses in StandardResponse format.
    This eliminates the need to override ViewSet methods while maintaining DRF capabilities.

    Usage in ViewSets:
    - Define custom success messages: success_messages = {'retrieve': 'Custom message', 'update': 'Another message'}
    - Define custom error messages: error_messages = {'400': 'Custom error message'}

    Response format:
    {
        "code": 200,
        "message": "Success message",
        "data": { /* your actual data */ },
        "status": "success"  # or "error"
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get("response")
        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        # Skip if already a StandardResponse
        if isinstance(response, StandardResponse):
            return super().render(data, accepted_media_type, renderer_context)

        # Determine message based on status code and method
        status_code = response.status_code
        request = renderer_context.get("request")
        method = request.method if request else "GET"
        view = renderer_context.get("view")

        message = self._get_message(status_code, method, view)

        # Wrap the response data in StandardResponse format
        wrapped_data = {
            "code": status_code,
            "message": message,
            "data": data,
            "status": "success" if 200 <= status_code < 300 else "error",
        }

        return super().render(wrapped_data, accepted_media_type, renderer_context)

    def _get_message(self, status_code, method, view):
        """Get appropriate message based on status code, HTTP method, and view configuration."""

        # Check for custom messages in the view
        if view and hasattr(view, "success_messages") and 200 <= status_code < 300:
            action = getattr(view, "action", None)
            if action and action in view.success_messages:
                return view.success_messages[action]

        if view and hasattr(view, "error_messages") and status_code >= 400:
            if str(status_code) in view.error_messages:
                return view.error_messages[str(status_code)]

        # Default messages
        if 200 <= status_code < 300:
            if method == "GET":
                return "Data retrieved successfully"
            elif method == "POST":
                return "Resource created successfully"
            elif method == "PUT":
                return "Resource updated successfully"
            elif method == "PATCH":
                return "Resource updated successfully"
            elif method == "DELETE":
                return "Resource deleted successfully"
            else:
                return "Success"
        elif status_code == 400:
            return "Bad request"
        elif status_code == 401:
            return "Unauthorized"
        elif status_code == 403:
            return "Forbidden"
        elif status_code == 404:
            return "Not found"
        elif status_code == 405:
            return "Method not allowed"
        elif status_code >= 500:
            return "Internal server error"
        else:
            return "Error"
