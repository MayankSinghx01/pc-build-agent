import dspy
from ddgs import DDGS

builder_lm = dspy.LM("gemini/gemini-3.5-flash-lite", api_key = "YOUR_API_KEY")
critic_lm = dspy.LM("gemini/gemini-3.5-flash-lite", api_key = "YOUR_API_KEY")


dspy.configure(lm=builder_lm)

class PCresearcher(dspy.Signature):

    """Search for a compatible, budget specific PC. Be concise. Improve from previous build"""

    previous_build: str = dspy.InputField()
    previous_avg_rating: float = dspy.InputField()
    previous_evaluation: str = dspy.InputField()

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()

    relevant_info: str = dspy.OutputField()

class PCBuilder(dspy.Signature):

    """Recommend a PC build. Be precise and to the point. Improve from previous build"""

    previous_build: str = dspy.InputField()
    previous_avg_rating: float = dspy.InputField()
    previous_evaluation: str = dspy.InputField()

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    researched_info: str = dspy.InputField()

    recommendation: str = dspy.OutputField()

class EvaluateBuild(dspy.Signature):

    """Give very precise evaluation. Be VERY STRICT IN YOUR RATING. Rate the build on the following parameters out of 10
    Do not trust the build blindly, verify important claims and ratings."""

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    recommendation: str = dspy.InputField()
    
    budget_eval: float = dspy.OutputField()
    compatibility_eval: float = dspy.OutputField()
    durability_eval: float = dspy.OutputField()
    gaming_performance_eval: float = dspy.OutputField()

    evaluation_summary: str = dspy.OutputField()

def web_search(query: str) -> str:
    results = DDGS().text(query, max_results = 5)
    return results

def calculate_total(component_prices: list[float]) -> float:
    return sum(component_prices)

def calculate_avg(list_of_ratings: list[float]) -> float:
    return sum(list_of_ratings)/len(list_of_ratings)

pc_researcher = dspy.ReAct(PCresearcher, tools = [web_search, calculate_total, calculate_avg])
pc_generator = dspy.Predict(PCBuilder)
pc_evaluator = dspy.Predict(EvaluateBuild)

b_in_r = 80000
req = "Power Supply, RAM, Storage, CPU, GPU"

iteration = 1
previous_build = ""
previous_evaluation = ""
previous_avg_rating = 0.0

while previous_avg_rating <= 9.0 and iteration <= 5:

    with dspy.context(lm = builder_lm):
        suggested_pc = pc_researcher(previous_build = previous_build, previous_avg_rating= previous_avg_rating, previous_evaluation = previous_evaluation, budget_in_rupees = b_in_r, requirements = req)
        built_pc = pc_generator(previous_build = previous_build, previous_avg_rating = previous_avg_rating, previous_evaluation = previous_evaluation, budget_in_rupees = b_in_r, requirements = req, researched_info = suggested_pc.relevant_info)

    with dspy.context(lm = critic_lm):
        eval_pc = pc_evaluator(budget_in_rupees = b_in_r, requirements = req, recommendation = built_pc.recommendation)

    previous_build = built_pc.recommendation
    previous_evaluation = eval_pc.evaluation_summary

    ratings = [
        eval_pc.budget_eval,
        eval_pc.compatibility_eval,
        eval_pc.durability_eval,
        eval_pc.gaming_performance_eval
    ]

    previous_avg_rating = calculate_avg(ratings)

    print(iteration)
    print(previous_avg_rating)
    print(eval_pc.evaluation_summary)

    iteration += 1

print(eval_pc.budget_eval)
print(eval_pc.compatibility_eval)
print(eval_pc.durability_eval)
print(eval_pc.gaming_performance_eval)

print(eval_pc.evaluation_summary)