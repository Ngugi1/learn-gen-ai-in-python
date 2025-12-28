# Prerequisite
- Microsoft Azure Subscription
- Python 3.14 or higher
# SetUp 
1. Declare Environment Variables
    - Open AI Credentials (can be found in Microsoft Foundry Model Deployment)
        - OPENAI_API_KEY="<api_key>"
        - OPENAI_MODEL="<model>"
        - OPENAI_END_POINT="<endpoint>"

    - Azure Open AI Credentials (can be found in a deployment of Azure Open AI resource)
        - AZURE_OPENAI_API_KEY = "<api_key>"
        - AZURE_OPENAI_ENDPOINT = "<endpoint>"
        - AZURE_OPENAI_API_VERSION="<version>"
        - AZURE_OPENAI_MODEL="<model>"

2. Create a python3 environment using command `python3 -m venv .packages_env`
3. Activate the just created `.packages_env` using command `source .packages_env/bin/activate`
4. In the activated environment (.packages_env), install dependencies listed in requirements.txt file using command `pip install -r requirements.txt`
- Run examples using command `python3 <filename>.py` e.g., `python3 01-azure-open-ai.py`
