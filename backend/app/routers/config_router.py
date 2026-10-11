"""This will expose configuration endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.get("/config")
def config(): raise HTTPException(status_code=501, detail="Not implemented")
