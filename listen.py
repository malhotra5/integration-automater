#!/usr/bin/env python3
import json
from datetime import datetime
import os

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
from jinja2 import FileSystemLoader, Environment
import json

load_dotenv()


INTEGRATION_NAME = "GitLab"
BRANCH_NAME = "gitlab-resolver"
FILE_NAME = "app/integrations/gitlab/gitlab_view.py"
TEMPLATE_FILE = "instructions.j2"

API_KEY = os.getenv("OPENHANDS_API_KEY")


app = FastAPI(title="Webhook Listener")


def load_instructions(payload):
    templateLoader = FileSystemLoader(searchpath="./")
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(
        integration_provider=INTEGRATION_NAME,
        branch_name=BRANCH_NAME,
        file_name=FILE_NAME,
        raw_payload=payload
    )

    return outputText


def create_oh_conversation(payload):
    url = "https://app.all-hands.dev/api/conversations"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    instructions = load_instructions(payload)

    data = {
        "initial_user_msg": instructions,
        "repository": "All-Hands-AI/deploy",
        "selected_branch": BRANCH_NAME
    }

    response = requests.post(url, headers=headers, json=data)
    conversation = response.json()

    print(conversation)

    print(f"Conversation Link: https://app.all-hands.dev/conversations/{conversation['conversation_id']}")
    print(f"Status: {conversation['status']}")



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
    
    # Print event details
    print("\n" + "="*50)
    print(f"⏰ EVENT RECEIVED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # print(load_instructions(json.dumps(data, indent=2)))

    create_oh_conversation(json.dumps(data, indent=2))

    print("="*50 + "\n")
    
    # Return a success response
    return {"status": "success", "message": "Event received"}


if __name__ == "__main__":
    print("🚀 Starting webhook listener server...")
    print("📡 Listening for events on port 3000")
    print("🔗 Forward this to your ngrok endpoint")
    print("💡 Press Ctrl+C to stop the server")
    uvicorn.run(app, host="0.0.0.0", port=3000)
