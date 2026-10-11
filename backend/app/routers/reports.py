"""This will expose report endpoints."""
from fastapi import APIRouter, HTTPException
router = APIRouter()
def not_implemented(): raise HTTPException(status_code=501, detail="Not implemented")
router.add_api_route("/report/summary-pdf", not_implemented, methods=["POST"])
router.add_api_route("/report/plan-pdf", not_implemented, methods=["POST"])
