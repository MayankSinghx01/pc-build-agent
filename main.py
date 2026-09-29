import dspy

lm = dspy.LM("gemini/gemini-3.5-flash-lite", api_key = "YOUR_API_KEY")

dspy.configure(lm=lm)

class PCresearcher(dspy.Signature):

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()

    relevant_info: str = dspy.OutputField()

class PCBuilder(dspy.Signature):

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    researched_info: str = dspy.InputField()

    recommendation: str = dspy.OutputField()

class EvaluateBuild(dspy.Signature):

    budget_in_rupees: int = dspy.InputField()
    requirements: str = dspy.InputField()
    recommendation: str = dspy.InputField()

    evaluation: str = dspy.OutputField()

pc_researcher = dspy.Predict(PCresearcher)
pc_generator = dspy.ChainOfThought(PCBuilder)
pc_evaluator = dspy.Predict(EvaluateBuild)

b_in_r = 80000
req = "Power Supply, RAM, Storage, CPU, GPU"

suggested_pc = pc_researcher(budget_in_rupees = b_in_r, requirements = req)
built_pc = pc_generator(budget_in_rupees = b_in_r, requirements = req, researched_info = suggested_pc.relevant_info)
eval_pc = pc_evaluator(budget_in_rupees = b_in_r, requirements = req, recommendation = built_pc.recommendation)

print (suggested_pc.relevant_info)
print(built_pc.recommendation)
print(eval_pc.evaluation)