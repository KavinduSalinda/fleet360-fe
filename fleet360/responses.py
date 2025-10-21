from rest_framework.response import Response


class StandardResponse(Response):
    def __init__(self, data=None, message="Success", code=200, pagination=None, **kwargs):
        payload = {
            "code": code,
            "message": message,
            "data": data,
            "status": "success" if 200 <= code < 300 else "error",
        }
        
        # Add pagination if provided
        if pagination is not None:
            payload["pagination"] = pagination
            
        super().__init__(payload, status=code, **kwargs)
