from typing import Any

class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400, data: Any = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data
