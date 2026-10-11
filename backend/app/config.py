"""This will load settings from environment variables."""
import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")
