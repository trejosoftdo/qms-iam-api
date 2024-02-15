"""Base API models
"""

from pydantic import BaseModel


class APIResponse(BaseModel):
    """API general response"""

    code: str
    type: str
    message: str
