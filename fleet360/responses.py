from rest_framework.response import Response


class StandardResponse(Response):
    def __init__(self, data=None, message="Success", code=200, **kwargs):
        payload = {
            "code": code,
            "message": message,
            "data": data,
            "status": "success" if 200 <= code < 300 else "error",
        }
        super().__init__(payload, status=code, **kwargs)
