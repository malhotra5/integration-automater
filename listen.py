#!/usr/bin/env python3
"""
A simple webhook listener for ngrok events.
This script creates a FastAPI server that listens on port 3000 and prints all incoming events.

Dependencies:
- fastapi
- uvicorn
- python-multipart (for form data)

Install with Poetry:
    poetry install

Or with pip:
    pip install fastapi uvicorn python-multipart
"""

import json
from datetime import datetime
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Webhook Listener")

@app.get("/")
async def home():
    """Root endpoint that confirms the server is running."""
    return {"message": "Webhook listener is running. Send POST requests to this endpoint to see them printed."}

@app.post("/")
async def webhook(request: Request):
    """Handle incoming webhook POST events and print them."""
    # Get the request data
    try:
        data = await request.json()
    except:
        try:
            data = await request.form()
            data = dict(data)
        except:
            data = await request.body()
            data = data.decode('utf-8')
    
    # Get headers
    headers = dict(request.headers)
    
    # Print event details
    print("\n" + "="*50)
    print(f"⏰ EVENT RECEIVED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 HEADERS: {json.dumps(headers, indent=2)}")
    print(f"📦 PAYLOAD: {json.dumps(data, indent=2) if isinstance(data, dict) else data}")
    print("="*50 + "\n")
    
    # Return a success response
    return {"status": "success", "message": "Event received"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    """Catch all other routes and methods."""
    # Get the request data
    try:
        data = await request.json()
    except:
        try:
            data = await request.form()
            data = dict(data)
        except:
            data = await request.body()
            data = data.decode('utf-8')
    
    # Get headers
    headers = dict(request.headers)
    
    # Get method
    method = request.method
    
    # Print event details
    print("\n" + "="*50)
    print(f"⏰ EVENT RECEIVED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 PATH: /{path}")
    print(f"🔄 METHOD: {method}")
    print(f"📝 HEADERS: {json.dumps(headers, indent=2)}")
    print(f"📦 PAYLOAD: {json.dumps(data, indent=2) if isinstance(data, dict) else data}")
    print("="*50 + "\n")
    
    # Return a success response
    return {"status": "success", "message": "Event received"}

if __name__ == "__main__":
    print("🚀 Starting webhook listener server...")
    print("📡 Listening for events on port 3000")
    print("🔗 Forward this to your ngrok endpoint")
    print("💡 Press Ctrl+C to stop the server")
    uvicorn.run(app, host="0.0.0.0", port=3000)
