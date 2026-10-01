import dspy
from ddgs import DDGS

lm = dspy.LM("gemini/gemini-3.5-flash-lite", api_key = "YOUR_API_KEY")

dspy.configure(lm=lm)

class PCresearcher(dspy.Signature):

    """Search for a compatible, budget specific PC. Be concise."""

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()

    relevant_info: str = dspy.OutputField()

class PCBuilder(dspy.Signature):

    """Recommend a PC build. Be precise and to the point."""

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    researched_info: str = dspy.InputField()

    recommendation: str = dspy.OutputField()

class EvaluateBuild(dspy.Signature):

    """Evaluate given PC build, be concise, specific and critical."""

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    recommendation: str = dspy.InputField()

    evaluation: str = dspy.OutputField()

def web_search(query: str) -> str:
    results = DDGS().text(query, max_results = 5)
    return results

def calculate_total(component_prices: list[float]) -> float:
    return sum(component_prices)

pc_researcher = dspy.ReAct(PCresearcher, tools = [web_search, calculate_total])
pc_generator = dspy.ReAct(PCBuilder, tools = [web_search, calculate_total])
pc_evaluator = dspy.ReAct(EvaluateBuild, tools = [web_search, calculate_total])

b_in_r = 80000
req = "Power Supply, RAM, Storage, CPU, GPU"

suggested_pc = pc_researcher(budget_in_rupees = b_in_r, requirements = req)
built_pc = pc_generator(budget_in_rupees = b_in_r, requirements = req, researched_info = suggested_pc.relevant_info)
eval_pc = pc_evaluator(budget_in_rupees = b_in_r, requirements = req, recommendation = built_pc.recommendation)

print (suggested_pc.relevant_info)
print("NEXT")
print(built_pc.recommendation)
[print("NEXT")]
print(eval_pc.evaluation)