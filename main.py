from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.legacy.query_pipeline import QueryPipeline
from prompts import context, code_parser_template
from code_reader import code_reader
from dotenv import load_dotenv
import os
import ast

load_dotenv()

llm = Ollama(model="mistral", request_timeout=30.0)

parser = LlamaParse(result_type="markdown")

file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()

embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm=llm)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="api_documentation",
            description="this gives documentation about code for an API. Use this for reading docs for the API",
        ),
    ),
    code_reader,
]

code_llm = Ollama(model="codellama")
agent = ReActAgent(tools=tools, llm=code_llm, verbose=True, system_prompt=context)


class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str


parser = PydanticOutputParser(CodeOutput)
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)
# Alternative approach - using simple function call instead of pipeline
def run_output_generation(response):
    prompt_str = json_prompt_tmpl.format_str(response=str(response))
    return llm.complete(prompt_str)

import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

async def run_interaction():
    while True:
        prompt = input("Enter a prompt (q to quit): ")
        if prompt == "q":
            break

        retries = 0

        while retries < 3:
            try:
                result = await agent.run(prompt)
                next_result = run_output_generation(response=result)
                cleaned_json = ast.literal_eval(str(next_result).replace("assistant:", ""))
                break
            except Exception as e:
                retries += 1
                print(f"Error occured, retry #{retries}:", e)

        if retries >= 3:
            print("Unable to process request, try again...")
            continue

        print("Code generated")
        print(cleaned_json["code"])
        print("\n\nDesciption:", cleaned_json["description"])

        filename = cleaned_json["filename"]

        try:
            with open(os.path.join("output", filename), "w") as f:
                f.write(cleaned_json["code"])
            print("Saved file", filename)
        except:
            print("Error saving file...")

# Run the async interaction
asyncio.run(run_interaction())
