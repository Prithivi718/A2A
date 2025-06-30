from llm.chat import chat_llm
from tools.exa_tool import search_using_exa, ExaSearchTool
from multi_agents.base_agent import BaseAgent


from typing_extensions import override
import ast,json

def tool_register():
    tool_info = []
    schema = ExaSearchTool.model_json_schema()
    tool_info.append({
        "query": schema["properties"]["query"],
        "num_results": schema["properties"]["num_results"]
    })

    return tool_info


class SearchSumAgent(BaseAgent):
    def __init__(self, Name: str, Model:str, Description: str, Instruction: str):
        self.name= Name
        self.model= Model
        self.description= Description
        self.instruction= Instruction

    @override
    def name(self) -> str:
        return self.name

    @override
    def description(self)-> str:
        return self.description

    @override
    def instruction(self)-> str:
        return self.instruction

    @override
    def model(self) -> str:
        return self.model


    @override
    def process_task(self, task:dict) -> str:
        user_query = task.get("query")
        if not user_query:
            return "No user query provided."

        # Prompt template for web-search & summarizer agent
        tool_info= tool_register()

        prompt = f"""
        You are a helpful AI agent. Your task is to extract structured arguments from the user's natural language query
        based on the schema of a known web search tool.

        ### Tool Schema:
        This tool expects the following arguments in JSON format:
        - "query": a clear search query string based on what the user is asking
        - "num_results": (optional) the number of search results to retrieve (default is 5)

        Here is the schema of the tool:
        {json.dumps(tool_info[0], indent=2)}

        ### User Query:
        "{user_query}"

        ### Task:
        1. Analyze the user's input to determine what topic or keywords they want to search for.
        2. If a specific number of results is requested, include it in "num_results".
        3. Return ONLY the arguments in this strict JSON format:
        
        ### Output Format
        Only return the JSON with no BackTicks. Do not add any explanation or extra text.
        {{
          "query": "search keywords here",
          "num_results": 5
        }}
        """

        llm_response = chat_llm(prompt, self.model)

        try:
            # Step 1: Parse JSON response from LLM
            parsed_args = ExaSearchTool(**json.loads(llm_response))  # validated input

            # Step 2: Call the tool with unpacked args
            result = search_using_exa(parsed_args)

            # Step 3: Return result as string
            return f"Searched Results:\n{result}"

        except Exception as e:
            return f"Error invoking tool: {e}"
