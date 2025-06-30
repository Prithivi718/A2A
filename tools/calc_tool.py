from pydantic import BaseModel, Field
from typing import List, Union, Literal

# ✅ Define input schema for the calculator using Pydantic
class CalcArgs(BaseModel):
    numbers: List[Union[int, float]] = Field(..., description="List of numbers to calculate")
    operation: Literal["add", "+", "subtract", "-", "multiply", "*", "divide", "/", "mod", "%"] = Field(..., description="Type of operation")

# ✅ Actual calculator function using the schema

def use_calculator(args: CalcArgs) -> Union[int, float, str]:
    """Performs a single operation for 'n' numbers of any data-type"""

    nums = args.numbers
    op = args.operation

    if not nums or len(nums) < 2:
        return "Error: Provide at least two numbers."

    result = nums[0]
    for num in nums[1:]:
        try:
            if op in ("add", "+"):
                result += num
            elif op in ("subtract", "-"):
                result -= num
            elif op in ("multiply", "*"):
                result *= num
            elif op in ("divide", "/"):
                result /= num
            elif op in ("mod", "%"):
                result %= num
        except Exception as e:
            return f"Error: {e}"

    return result
        