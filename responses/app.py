import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

print("\n🔹 AI Business Assistant is ready. Ask me anything about your business!")
print("🔹 Type 'exit' to quit.\n")

while True:
    # Get user input
    user_query = input("You: ")

    # Exit condition
    if user_query.lower() in ["exit", "quit"]:
        print("🔹 Exiting chat. Goodbye!")
        break

    # Send user query to OpenAI
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_query  # Pass the user's question dynamically
                    }
                ]
            }
        ],
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [
                    "vs_67dc25727efc81919e3195edcc24e461"  # Your vector store for business data
                ]
            }
        ],
        temperature=1,
        max_output_tokens=1500,
        top_p=1
    )

    # ✅ Ensure response prints for each input
    print("\n🔹 AI Assistant Response:\n", response.output_text, "\n")