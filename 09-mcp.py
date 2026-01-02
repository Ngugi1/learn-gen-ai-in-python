from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import asyncio

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",
            "command": "python3",
            "args": ["/Users/sam/Documents/AgenticAI/learn-gen-ai-in-python/09-mcp-math.py"]
        },
        "weather": {
            "transport": "http",
            "url": "http://127.0.0.1:8000/mcp"
        }
    }
)


async def invoke_agent():
    tools = await client.get_tools()
    model = ChatOllama(model="gpt-oss:20b")
    agent = create_agent(tools=tools, model=model)
    math_result = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
    print("Math+++++++++++",math_result)
    weather_result = await agent.ainvoke({"messages": [{"role": "user", "content": "What is the weather like in New York?"}]})
    print("Weather+++++++++++",weather_result)
if __name__ == "__main__":
    result = asyncio.run(invoke_agent())

