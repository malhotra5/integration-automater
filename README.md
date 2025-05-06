# integration-automater using openhands api

This repo helps you automate building integrations using the openhands api

It receives webhook payloads from the integration, and sends that details to an openhands agent. The agent will inspect the payload and build an integration that can handle the payload format, details, etc.

## Webhook Listener

The `listen.py` script provides a simple webhook listener for ngrok events. It listens on port 3000 and prints all incoming events to the console.

### Installation

This project uses Poetry for dependency management. To install the required dependencies:

```bash
# Install Poetry if you don't have it already
# curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Alternatively, you can install dependencies directly with pip
# pip install fastapi uvicorn python-multipart
```

### Usage

1. Start your ngrok tunnel pointing to port 3000:

   ```bash
   ngrok http 3000
   ```

2. Run the webhook listener:

   ```bash
   poetry run python listen.py
   ```

3. Send webhook events to your ngrok URL, and they will be printed in the console.

### Features

- Listens on port 3000 for incoming webhook events
- Supports JSON, form data, and raw request bodies
- Prints detailed information about each request including:
  - Timestamp
  - Headers
  - Path
  - HTTP method
  - Request payload
