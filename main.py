from openai import OpenAI
from pypdf import PdfReader
import os

# ==========================================
# CONFIG
# ==========================================
from openai import OpenAI
from pypdf import PdfReader
import os

# ==========================
# MORPH CONFIG
# ==========================

API_KEY = "sk-R2OGPh7B2xUoKm-WqYgdKHoPxNB4xoQtB6pIkQMBsOh0S40T"

client = OpenAI(
    base_url="https://api.morphllm.com/v1",
    api_key=API_KEY,
)

MODEL = "morph-v3-fast"

# ==========================================
# LOAD PDF
# ==========================================

print("=" * 60)
print("🤖 AI PDF CHAT")
print("=" * 60)

while True:
    pdf_path = input("\nEnter PDF file name/path: ").strip().strip('"')

    if os.path.exists(pdf_path):
        break

    print("❌ File not found. Please try again.")

try:
    reader = PdfReader(pdf_path)

    pdf_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

except Exception as e:
    print("Error loading PDF:", e)
    exit()

print("\n✅ PDF Loaded Successfully!")
print("📄 PDF:", os.path.basename(pdf_path))
print(f"📚 Characters Loaded: {len(pdf_text)}")

# ==========================================
# CREATE CHAT HISTORY
# ==========================================

messages = [
    {
        "role": "system",
        "content": f"""
You are an AI assistant.

Answer ONLY from the PDF below.

If the answer does not exist inside the PDF,
reply exactly:

'I could not find that information in the PDF.'

================ PDF =================

{pdf_text}

======================================
"""
    }
]

print("\nYou can now ask questions about the PDF.")
print("Type 'exit' to quit.")
print("-" * 60)

# ==========================================
# CHAT LOOP
# ==========================================

while True:

    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    if question == "":
        continue

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
        )

        answer = response.choices[0].message.content

        print("\nAI:", answer)

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        print("\n❌ Error:", e)
        
