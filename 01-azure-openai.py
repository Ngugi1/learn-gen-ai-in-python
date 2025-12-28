# Hello world from gpt-5-nano using Azure OpenAI API
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Get credentials from .env file
load_dotenv()

# Instantiate the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["OPENAI_API_KEY"],
    api_version=os.environ['AZURE_OPENAI_API_VERSION']
)
# Create a chat completion messages
messages = [
    {
        "role": "user",
        "content": "What is the capital of France?",
    }
]
# Create a chat completion
completion = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_MODEL"],
    messages=messages,
)

# Print the responses
for choice in completion.choices:
    print(choice.message.content)   