from langchain_anthropic import ChatAnthropic
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

# Initialize the model
llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    timeout=100, # Increase for complex tasks
)
async def main():
    agent = Agent(
        task="List out all the IPADs with their price and processor",
        LLm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
