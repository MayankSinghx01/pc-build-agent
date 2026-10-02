# pc-build-agent
Using DSPy to build a PC Recommendation System.

**LLM Used**: gemini-3.5-flash-lite (decent performance with low traffic)

1. v1.0: PC builder agent that takes budget and requirements as input and gives recommended system as output.
2. v1.1: PC builder agent that takes budget and requremetns as input, passes it on to a researcher that collects relevant information, passes it to builder to get final specs and then passes it on to an evaluator that judges the final pc
3. v1.2: PC builder agent with **basic tools** for searching the internet or calculating total price.
4. v1.3: PC builder agent with an evaluation metric for judging the final pc specs and implementing a loop to improve evaluated score and build the best possible pc. (YET TO IMPLEMENT)
