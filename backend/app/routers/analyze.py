"""This will expose analysis endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
def not_implemented(): raise HTTPException(status_code=501, detail="Not implemented")
router.add_api_route("/analyze/spoken", not_implemented, methods=["POST"])
router.add_api_route("/analyze/paragraph", not_implemented, methods=["POST"])
router.add_api_route("/analyze/ratings", not_implemented, methods=["POST"])
