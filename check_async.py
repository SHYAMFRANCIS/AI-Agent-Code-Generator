import asyncio
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool

def test_func():
    """Test function"""
    return "test"

# Create a simple tool
test_tool = FunctionTool.from_defaults(fn=test_func)

# Create an Ollama LLM instance
llm = Ollama(model="mistral")

# Create the agent
agent = ReActAgent(tools=[test_tool], llm=llm)

print("Available methods on agent:")
methods = [method for method in dir(agent) if not method.startswith('_') and callable(getattr(agent, method))]
async_methods = [m for m in methods if m.startswith('a')]  # look for async methods
other_methods = [m for m in methods if 'run' in m.lower()]

print(f"Async-methods (starting with 'a'): {async_methods}")
print(f"All run-related methods: {other_methods}")

# Let's also test if the run method is actually a coroutine
result = agent.run("test")
print(f"Result of agent.run(): {type(result)}")
print(f"Is coroutine?: {asyncio.iscoroutine(result)}")

if asyncio.iscoroutine(result):
    print("Run method returns a coroutine - it should be awaited")
else:
    print("Run method does not return a coroutine")