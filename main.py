from openai import OpenAI
import json
import os

# =====================================
# CONFIG
# =====================================

API_KEY = "sk-R2OGPh7B2xUoKm-WqYgdKHoPxNB4xoQtB6pIkQMBsOh0S40T"

client = OpenAI(
    base_url="https://api.morphllm.com/v1",
    api_key=API_KEY,
)

MODEL = "morph-v3-fast"

HISTORY_FILE = "history.json"

SYSTEM_PROMPT = (
    "You are a helpful AI assistant."
)

# =====================================
# LOAD CHAT HISTORY
# =====================================

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# =====================================
# SAVE FUNCTION
# =====================================

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)

# =====================================
# START
# =====================================

print("=" * 60)
print("🤖 Morph AI Chatbot")
print("Commands:")
print("exit    -> Quit")
print("reset   -> Clear history")
print("history -> Show conversation")
print("=" * 60)

# =====================================
# CHAT LOOP
# =====================================

while True:

    user_input = input("\nYou: ").strip()

    if user_input == "":
        continue

    cmd = user_input.lower()

    # Exit
    if cmd == "exit":
        save_history()
        print("Conversation saved.")
        break

    # Reset
    if cmd == "reset":
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        save_history()
        print("Conversation cleared.")
        continue

    # Show history
    if cmd == "history":
        print("\n----------- HISTORY -----------")
        for msg in messages:
            if msg["role"] == "system":
                continue
            print(f"{msg['role'].capitalize()}: {msg['content']}")
        print("-------------------------------")
        continue

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        reply = response.choices[0].message.content

        print("\nMorph:", reply)

        messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        save_history()

    except Exception as e:
        print("\nError:", e)