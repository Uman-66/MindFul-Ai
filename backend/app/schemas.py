"""This will define API Pydantic schemas."""
from pydantic import BaseModel
class Config(BaseModel): pass
class Indicator(BaseModel): pass
class BranchResult(BaseModel): pass
class SpokenResult(BaseModel): pass
class VideoBranch(BaseModel): pass
class FuseRequest(BaseModel): pass
class FusedResult(BaseModel): pass
class ResourcesResult(BaseModel): pass
class PlanResult(BaseModel): pass
class ChatRequest(BaseModel): pass
class ErrorResponse(BaseModel): pass
