"""This will expose fusion endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.post("/fuse")
def fuse(): raise HTTPException(status_code=501, detail="Not implemented")
