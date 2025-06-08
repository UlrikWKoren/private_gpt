# Private GPT

This project provides both a command-line and web interface to interact with various chat models. Messages are streamed so you can see responses in real time. You can also edit any earlier user message and resend the conversation.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your API keys as needed. For example:

```bash
export OPENAI_API_KEY=YOUR_OPENAI_KEY
export AZURE_OPENAI_API_KEY=YOUR_AZURE_KEY
export AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE.azure.com/
export AZURE_OPENAI_DEPLOYMENT=YOUR_DEPLOYMENT
export GEMINI_API_KEY=YOUR_GEMINI_KEY
export ANTHROPIC_API_KEY=YOUR_CLAUDE_KEY
```

## Usage

### Command Line

Run the chat interface:

```bash
python chatgpt_local.py
```

Type your message to send it to the model. Use `edit <index>` to edit a previous user message and resend the conversation. Type `quit` to exit.

### Web Application

Start the Flask server:

```bash
python webapp.py
```

Open `http://localhost:5000` in your browser. The UI uses [Bifrost Design System](https://bifrost.intility.com/). Select a provider, send messages and edit earlier ones using the *Edit* links next to each user message.
