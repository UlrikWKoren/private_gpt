import os
from flask import Flask, request, redirect, url_for, render_template_string
import openai
import google.generativeai as genai
import anthropic

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang=\"en\" class=\"bf-theme-purple\">
<head>
  <meta charset=\"utf-8\">
  <title>Local ChatGPT</title>
  <link rel=\"stylesheet\" href=\"https://unpkg.com/@intility/bifrost-css@latest/dist/bifrost-all.css\">
</head>
<body class=\"bf-page-padding\">
  <h1 class=\"bf-h2 bfc-theme\">Local ChatGPT</h1>
  <form action=\"{{ url_for('send') }}\" method=\"post\" style=\"display:flex;flex-direction:column;gap:0.5rem;\">
    <select name=\"provider\" class=\"bf-select\">
      {% for p in providers %}
      <option value=\"{{ p }}\" {% if p==provider %}selected{% endif %}>{{ p }}</option>
      {% endfor %}
    </select>
    <textarea name=\"message\" rows=\"4\" class=\"bf-textarea\" required>{{ edit_text }}</textarea>
    <input type=\"hidden\" name=\"edit_index\" value=\"{{ edit_index }}\">
    <button type=\"submit\" class=\"bf-button primary\">Send</button>
  </form>
  <ul class=\"bf-elements\" style=\"margin-top:1rem;\">
  {% for i, m in enumerate(messages) %}
    <li class=\"bf-padding bfc-base-3-bg bf-rounded\">
      <strong>{{ m['role'] }}</strong>: {{ m['content'] }}
      {% if m['role'] == 'user' %}
        <a href=\"{{ url_for('edit', index=i) }}\" class=\"bf-link\">Edit</a>
      {% endif %}
    </li>
  {% endfor %}
  </ul>
</body>
</html>
"""

class ChatSession:
    def __init__(self):
        self.provider = 'openai'
        self.messages = []

def available_providers():
    return ['openai', 'azure', 'gemini', 'claude']

session = ChatSession()

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        messages=session.messages,
        provider=session.provider,
        providers=available_providers(),
        edit_index='',
        edit_text=''
    )

@app.route('/send', methods=['POST'])
def send():
    text = request.form['message']
    provider = request.form['provider']
    edit_index = request.form.get('edit_index')

    if edit_index:
        idx = int(edit_index)
        if 0 <= idx < len(session.messages) and session.messages[idx]['role'] == 'user':
            session.messages[idx]['content'] = text
            session.messages = session.messages[: idx + 1]
    else:
        session.messages.append({'role': 'user', 'content': text})

    session.provider = provider
    answer = call_provider(provider, session.messages)
    session.messages.append({'role': 'assistant', 'content': answer})
    return redirect(url_for('index'))

@app.route('/edit/<int:index>')
def edit(index: int):
    if index >= len(session.messages) or session.messages[index]['role'] != 'user':
        return redirect(url_for('index'))
    return render_template_string(
        HTML_TEMPLATE,
        messages=session.messages,
        provider=session.provider,
        providers=available_providers(),
        edit_index=index,
        edit_text=session.messages[index]['content']
    )

def call_provider(name: str, messages: list) -> str:
    if name == 'openai':
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            return '[OPENAI_API_KEY missing]'
        client = openai.OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        return resp.choices[0].message.content

    if name == 'azure':
        key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        if not all([key, endpoint, deployment]):
            return '[Azure OpenAI config missing]'
        client = openai.AzureOpenAI(api_key=key, azure_endpoint=endpoint, api_version=version)
        resp = client.chat.completions.create(model=deployment, messages=messages)
        return resp.choices[0].message.content

    if name == 'gemini':
        key = os.getenv('GEMINI_API_KEY')
        if not key:
            return '[GEMINI_API_KEY missing]'
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        history = [{'role': m['role'], 'parts': [m['content']]} for m in messages]
        resp = model.generate_content(history)
        return resp.text

    if name == 'claude':
        key = os.getenv('ANTHROPIC_API_KEY')
        if not key:
            return '[ANTHROPIC_API_KEY missing]'
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model='claude-3-sonnet-20240229',
            max_tokens=1024,
            messages=messages
        )
        return ''.join(block.text for block in resp.content)

    return '[Unsupported provider]'

if __name__ == '__main__':
    app.run(debug=True)
