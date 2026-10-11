"""This will expose the server-sent chat endpoint."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
@router.post("/chat")
def chat(): raise HTTPException(status_code=501, detail="Not implemented")
