# prompts.py
BASE_PROMPT = """You are a helpful math assistant.
Solve the following problem. Always show your reasoning briefly.
Then output ONLY the final numeric answer prefixed EXACTLY by:

#### ANSWER: <number>

Question:
{question}

#### ANSWER:"""

ROLE_COT_PROMPT = """You are a patient math tutor who explains reasoning step by step.
Show your steps clearly, then output ONLY the final numeric answer prefixed EXACTLY by:

#### ANSWER: <number>

Question:
{question}

Solution and reasoning:
#### ANSWER:"""

FEW_SHOT_PROMPT = """You are a math tutor. Follow the examples below and obey the answer format exactly.

Example 1:
Q: If you have 3 apples and get 2 more, how many apples?
A: 3 + 2 = 5
#### ANSWER: 5

Example 2:
Q: If a car travels 60 miles in 1.5 hours, what is the average speed?
A: 60 / 1.5 = 40
#### ANSWER: 40

Now solve:
Question:
{question}

Answer (remember to end with '#### ANSWER: <number>'):
#### ANSWER:"""

# prompts.py (add to bottom)

# Self-consistency prompt
SELF_CONSISTENCY_PROMPT = """You are a careful math tutor.
Solve the problem step by step and provide three possible reasoning paths.
Then decide which path leads to the most confident final numeric answer.
Output the final numeric answer at the end prefixed EXACTLY by '#### ANSWER:'.

Question:
{question}

Reasoning paths:
#### ANSWER:"""

# Meta-prompt (reflective reasoning)
META_PROMPT = """You are a reflective math tutor.
Before solving, think about what reasoning strategy is best for this problem.
Then solve carefully step by step.
Output the final numeric answer at the end prefixed EXACTLY by '#### ANSWER:'.

Question:
{question}

Strategy and solution:
#### ANSWER:"""
