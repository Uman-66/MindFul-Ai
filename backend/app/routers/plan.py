"""This will expose support plan endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.post("/plan")
def plan(): raise HTTPException(status_code=501, detail="Not implemented")
