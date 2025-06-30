from multi_agents.calc_agent import CalculatorAgent # your tool class
from multi_agents.search_sum_agent import SearchSumAgent

from typing import Dict, Any

from llm.chat import chat_llm

class Orchestrator:
    def __init__(self):
        self.agents: Dict[str, Any] = {}

    def register_agent(self, task_type: str, agent):
        self.agents[task_type] = agent

    def classify_task_type(self, user_query: str) -> str:
        prompt = f"""
            You are a task classifier agent. Classify the user's query into one of the following task types:
            - "math" → for math calculations (e.g. add, subtract, divide, etc.)
            - "search" → for information lookup, summarization, or general knowledge

            User query:
            "{user_query}"

            Respond ONLY with one word: "math" or "search"
        """
        task_response = chat_llm(prompt)
        return task_response.strip().lower()

    def route_task(self, tasks: Dict) -> Dict:
        user_query = tasks.get("query", "")
        if not user_query:
            return {"error": "No query provided"}

        task_type = self.classify_task_type(user_query)
        agent = self.agents.get(task_type)

        if not agent:
            return {"error": f"No agent registered for task type: {task_type}"}

        return {"result": agent.process_task(tasks)}





# Initialize agent with tool
calc_agent = CalculatorAgent(
    Name="CalcAgent",
    Model="gpt-4o-mini",
    Description="Solves math tasks",
    Instruction="Use tool for arithmetic.",
)

search_sum_agent = SearchSumAgent(
    Name="SearchSumAgent",
    Model="gpt-4o-mini",
    Description="Searches the web for information and summarizes it",
    Instruction="Use tool for web search and summarization.",
)


# Orchestrator
orch = Orchestrator()
orch.register_agent("math", calc_agent)
orch.register_agent("search", search_sum_agent)

# Run time query
query = input("You: ")
task = {"query": query}
result = orch.route_task(task)

print("🤖 Agent Reply:\n", result.get("result", result.get("error")))