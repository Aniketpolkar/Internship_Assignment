from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain.agents import create_agent
from langchain_groq import ChatGroq 
from dotenv import load_dotenv

import asyncio 
 
load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathServer.py"],#ensure correct absolute path
                "transport":"stdio",
            },

            "MCPServer":{
               "url":"http://localhost:8000/mcp",# Ensure the server is running here
               "transport":"streamable_http",
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()

    model = ChatGroq(model="openai/gpt-oss-20b")

    agent = create_agent(
        model,tools
    )
   
    tool_response = await agent.ainvoke({
         "messages": [
        {
            "role": "system",
            "content": "You must use the provided tools to answer. Do not answer from your own knowledge. Give in short"
        },
        {
            "role": "user",
            "content": "Give me the only list of forts from my mongodb database. which are built by chhatrapti shivaji maharaj."
        }
        ]
         })

    print("tool response:",tool_response["messages"][-1].content)

asyncio.run(main())
