# from openai import AzureOpenAI
# import os
# from dotenv import load_dotenv  
# # Load environment variables from .env file
# load_dotenv()
# # Instantiate the Azure OpenAI client
# azure_open_ai_client = AzureOpenAI(
#     api_version=os.environ["AZURE_OPENAI_API_VERSION"],
#     base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
#     api_key=os.environ["OPENAI_API_KEY"]
# )

# # Create an embeddings
# embeddings = azure_open_ai_client.embeddings.create(
#     model= os.environ["OPENAI_EMBEDDING_MODEL"],
#     input=["hello world", "goodbye world"]
# )

# for i, e in enumerate(embeddings.data):
#     print(f"Embedding {i}: {e.embedding[:5]}...")  # Print first 5 values of each embedding

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
model_name =os.environ["OPENAI_EMBEDDING_MODEL"]

api_version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.embeddings.create(
    input=["first phrase","second phrase","third phrase"],
    model=model_name
)

for item in response.data:
    length = len(item.embedding)
    print(
        f"data[{item.index}]: length={length}, "
        f"[{item.embedding[0]}, {item.embedding[1]}, "
        f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
    )
print(response.usage)