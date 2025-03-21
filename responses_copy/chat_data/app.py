import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the AI Business Assistant API!"

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Call OpenAI's API using your assistant (adjust model and parameters as needed)
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_query
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
                    "vs_67dc25727efc81919e3195edcc24e461"
                ]
            }
        ],
        temperature=1,
        max_output_tokens=1500,
        top_p=1
    )

    # Extract the assistant's response from the output list
    assistant_text = None
    for item in response.output:
        # Check if it's a ResponseOutputMessage (adjust attribute access as needed)
        if hasattr(item, "content") and item.content:
            assistant_text = item.content[0].text
            break

    if not assistant_text:
        return jsonify({"error": "No response from AI assistant"}), 500

    return jsonify({"response": assistant_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Must use 8080 for Cloud Run
    app.run(host='0.0.0.0', port=port)