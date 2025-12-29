
import json
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
load_dotenv()


client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["OPENAI_API_KEY"],
    api_version=os.environ['AZURE_OPENAI_API_VERSION']
)
# Define the function schemas for the functions we want the model to call
functions = [
    {
        "name": "search_courses",
        "description": "Retrieves courses from the search index based on the parameters provided",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "The role of the learner (i.e. developer, data scientist, student, etc.)"
                },
                "product": {
                    "type": "string",
                    "description": "The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
                },
                "level": {
                    "type": "string",
                    "description": "The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
                }
            }
        },
        "required": ["role"]
    }
]

def search_courses(role, product, level):
  url = "https://learn.microsoft.com/api/catalog/"
  params = {
     "role": role,
     "product": product,
     "level": level
  }
  response = requests.get(url, params=params)
  print("API Response Status Code:", response.status_code)
  print("API Response Content:", response.text) 
  modules = response.json()["modules"]
  results = []
  for module in modules[:5]:
     title = module["title"]
     url = module["url"]
     results.append({"title": title, "url": url})
  return str(results)

# Package the function into a dictionary for easy lookup
available_functions = {
    "search_courses": search_courses
}
# Create the initial message
messages = [
    {
        "role": "user",
        "content": "Find me a good course for a beginner student to learn Azure."
    }
]
# Make the initial chat completion request
response = client.chat.completions.create(
    model=os.environ["OPENAI_MODEL"],
    messages=messages,
    functions=functions,
    function_call="auto"
)
# Extract the function call from the response
fn_call = response.choices[0].message.function_call

if fn_call and fn_call.name in available_functions:
    # Find the function to call
    function_to_call = available_functions[fn_call.name]
    function_args = json.loads(fn_call.arguments)
    function_response = function_to_call(**function_args)
    # Append the function response to the messages
    messages.extend([
           {
                "role": response.choices[0].message.role,
                "content": response.choices[0].message.content,
                "function_call": {
                    "name": fn_call.name,
                    "arguments": fn_call.arguments
                }
            },
            {
                "name": fn_call.name,
                "content": function_response
            }
        ])
    final_response = client.chat.completions.create(
        model=os.environ["OPENAI_MODEL"],
        functions=functions,
        messages=messages,
        function_call="auto",
        temperature=0
    )
    print(final_response.choices[0].message.content)




