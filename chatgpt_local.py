import os
import openai

SYSTEM_PROMPT = "You are ChatGPT, a large language model."  # default system message

class ChatSession:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("Set OPENAI_API_KEY in your environment.")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def display(self):
        for idx, msg in enumerate(self.messages):
            role = msg["role"]
            if role == "user":
                print(f"{idx}: {msg['content']}")
            elif role == "assistant":
                print(f"   Assistant: {msg['content'][:60]}")

    def send(self):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )
        answer = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                answer += delta
        print()
        self.messages.append({"role": "assistant", "content": answer})

    def edit(self, index: int, new_content: str):
        if index < 0 or index >= len(self.messages):
            print("Invalid index")
            return
        if self.messages[index]["role"] != "user":
            print("You can only edit user messages")
            return
        self.messages[index]["content"] = new_content
        # remove all messages after the edited one
        self.messages = self.messages[: index + 1]
        self.send()

def main():
    session = ChatSession()
    while True:
        session.display()
        inp = input("Enter message (or 'edit <index>'/quit): ")
        if inp.strip().lower() == "quit":
            break
        if inp.startswith("edit "):
            try:
                idx = int(inp.split()[1])
            except (IndexError, ValueError):
                print("Usage: edit <index>")
                continue
            new_msg = input("New message: ")
            session.edit(idx, new_msg)
        else:
            session.messages.append({"role": "user", "content": inp})
            session.send()

if __name__ == "__main__":
    main()
