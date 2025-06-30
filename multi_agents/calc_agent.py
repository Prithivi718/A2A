from js2py.internals.prototypes.jsjson import indent
from llm.chat import chat_llm
from typing_extensions import override
from multi_agents.base_agent import BaseAgent
import json, ast
from tools.calc_tool import use_calculator, CalcArgs


def tool_register():
    tool_info = []
    schema = CalcArgs.model_json_schema()
    tool_info.append({
        "numbers": schema["properties"]["numbers"],
        "operation": schema["properties"]["operation"]
    })

    return tool_info



class CalculatorAgent(BaseAgent):
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

        tool_info= tool_register()

        # Prompt template for LLM to extract structured task
        prompt = f"""
        You are a helpful AI agent. Your task is to extract structured arguments from the user's natural language query
        based on the schema of a known tool.

        ### Tool Schema:
        This tool expects the following arguments in JSON format:
        - "numbers": a list of numeric values (integers or floats) to be calculated
        - "operation": the type of math operation to perform (can be a word like "add" or symbol like "+")

        Here is the schema of the tool:
        {json.dumps(tool_info[0], indent=2)}

        ### User Query:
        "{user_query}"

        ### Task:
        1. Analyze the user query.
        2. Extract the relevant values that match the tool's expected arguments.
        3. Return ONLY the arguments in this strict JSON format:

        ### Output Format:
         Only return the JSON with no Backticks. Do not add any explanation or extra text.
            {{  
              "numbers": [number1, number2, ...],
              "operation": "operation_string"
            }}

        """

        llm_response = chat_llm(prompt, self.model)
        try:
            # Step 1: Parse JSON response from LLM
            parsed_args = CalcArgs(**json.loads(llm_response))  # validated input

            # Step 2: Call the tool with unpacked args
            result = use_calculator(parsed_args)

            # Step 3: Return result as string
            return f"Result: {result}"

        except Exception as e:
            return f"Error invoking tool: {e}"

