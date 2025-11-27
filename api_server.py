#!/usr/bin/env python3
"""
API server entry point for the web application.
Run with: uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
"""
import uvicorn
from src.api import app

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

