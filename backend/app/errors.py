"""This will define standard error responses."""
from pydantic import BaseModel
class ErrorResponse(BaseModel):
    error: dict
