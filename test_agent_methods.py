from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool

# Create a simple function to test with ReActAgent
def test_func():
    """Test function"""
    return "test"

# Create a simple tool
test_tool = FunctionTool.from_defaults(fn=test_func)

# Create an Ollama LLM instance
llm = Ollama(model="mistral")

# Create the agent
agent = ReActAgent(tools=[test_tool], llm=llm)

print("Methods available on ReActAgent:")
methods = [method for method in dir(agent) if not method.startswith('_') and callable(getattr(agent, method))]
print(methods)

print()
print("Methods with relevant names:")
relevant = [m for m in methods if any(keyword in m.lower() for keyword in ['run', 'chat', 'query', 'invoke', 'call', 'step'])]
print(relevant)

# Check if the agent supports the __call__ method
print()
print("Agent is an instance of:", type(agent))