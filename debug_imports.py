import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)

try:
    from llama_index.llms.ollama import Ollama
    print("SUCCESS: Ollama imported successfully")
except ImportError as e:
    print("ERROR importing Ollama:", e)

try:
    from llama_index.core.query_engine import BaseQueryEngine
    print("SUCCESS: BaseQueryEngine imported successfully")
except ImportError as e:
    print("ERROR importing BaseQueryEngine:", e)

try:
    from llama_index.legacy.query_pipeline import QueryPipeline
    print("SUCCESS: QueryPipeline imported successfully")
except ImportError as e:
    print("ERROR importing QueryPipeline:", e)

try:
    import llama_parse
    print("SUCCESS: llama_parse imported successfully")
except ImportError as e:
    print("ERROR importing llama_parse:", e)