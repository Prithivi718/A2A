from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
import os

try:
    from exa_py import Exa
except ImportError:
    raise ImportError("Missing Exa module!! Install module by `pip install exa_py`")

exa_api_key= os.getenv("EXA_API_KEY")
exa= Exa(api_key= exa_api_key)

class ExaSearchTool(BaseModel):
    query: str
    num_results: Optional[int]= Field(default=5, description="Number of search results for the given query")

def search_using_exa(params: ExaSearchTool):
    parsed = []
    try:
        search_results= exa.search_and_contents(query= params.query, num_results= params.num_results)

        for item in search_results.results:
            parsed.append({
                "title": item.title,
                "url": item.url,
                "snippet": item.text[:300]  # trimmed content
            })

    except Exception as e:
        print(f"\nError: {e}\n")

    return parsed