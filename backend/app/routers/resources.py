"""This will expose resource lookup endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.post("/resources/lookup")
def lookup(): raise HTTPException(status_code=501, detail="Not implemented")
