# Private GPT

This project provides a minimal command-line interface to interact with OpenAI's chat models. Messages are streamed so you can see the model respond in real time. You can also edit any earlier user message and resend the conversation.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=YOUR_KEY
```

## Usage

Run the chat interface:

```bash
python chatgpt_local.py
```

Type your message to send it to the model. Use `edit <index>` to edit a previous user message (based on the index shown) and resend the conversation. Type `quit` to exit.
