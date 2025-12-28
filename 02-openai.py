# Hello world from LLM using OpenAI API
import os
from openai import OpenAI
from dotenv import load_dotenv

# Get credentials from .env file
load_dotenv()
# Instantiate the OpenAI client
open_ai_client = OpenAI(
    base_url=os.environ["OPENAI_END_POINT"],
    api_key=os.environ["OPENAI_API_KEY"]
)

# Define the messages for the chat completion
messages =[
    {
        "role": "user",
        "content": "What is the capital of France?",
    }
]

# Create a chat completion
completion = open_ai_client.chat.completions.create(
    model=os.environ["OPENAI_MODEL"],
    messages=messages
)

# Print the response
print(completion.choices[0].message.content)