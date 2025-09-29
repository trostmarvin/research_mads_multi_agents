# MADS (Multi-Agent Documentation System) - Prototype Cycle 1
# This script implements the first proof of concept.
# Focus: Code analysis and text generation with two agents.

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
# from google.colab import userdata
from dotenv import load_dotenv

# Retrieve the API key from Colab's secrets manager
# os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")

# Load from .env
load_dotenv()

# Select LLM model for agents (e.g. gpt-4o-mini, gpt-4-turbo)
llm = ChatOpenAI(model="gpt-4o-mini")


# --- EXAMPLE CODE TO ANALYZE ---
# This is the Python project that our agents should analyze.
# For Cycle 1, it's just a single function for testing.
code_to_analyze = """
def calculate_fibonacci(n, memo=None):
    \"\"\"This function has no docstring yet.\"\"\"
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        result = calculate_fibonacci(n - 1, memo) + calculate_fibonacci(n - 2, memo)
        memo[n] = result
        return result
"""


# --- AGENT DEFINITIONS (according to Phase 2 of the plan) ---

# 1. CodeAnalysisAgent: Analyzes the code
code_analysis_agent = Agent(
    role='Senior Python Code Analyst',
    goal='Analyze a given Python function and extract its purpose, parameters, and return values.',
    backstory=(
        "You are an experienced software developer with a sharp eye for details. "
        "Your strength lies in breaking down complex code and understanding and summarizing its core logic "
        "in a clear, structured way. You form the foundation for any good documentation."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. WriterAgent: Writes the documentation
writer_agent = Agent(
    role='Technical Editor for Python Documentation',
    goal='Create a precise and well-formatted docstring in Google style based on code analysis.',
    backstory=(
        "You are an expert in creating technical documentation. "
        "Your motto is: 'Good code documents itself, but excellent code is documented by you.' "
        "You transform dry code analyses into understandable and useful docstrings that make other developers' lives easier."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)


# --- TASK DEFINITIONS (according to Phase 3, Cycle 1) ---

# Task 1: Analyze code
# The `CodeAnalysisAgent` receives the code and the task to analyze it.
analysis_task = Task(
    description=(
        "Analyze the following Python function:\n\n"
        f"```python\n{code_to_analyze}\n```\n\n"
        "Identify and describe the following points:\n"
        "1. The overall purpose of the function.\n"
        "2. All parameters (arguments), their type and what they represent.\n"
        "3. What the function returns, including the type of the return value."
    ),
    expected_output=(
        "A structured text analysis that clearly presents the purpose, parameters (Args), and return value (Returns) of the function."
    ),
    agent=code_analysis_agent
)

# Task 2: Write docstring
# The `WriterAgent` receives the analysis from Task 1 (this happens automatically via `context`)
# and the task to write the docstring.
writing_task = Task(
    description=(
        "Use the provided code analysis to create a complete and "
        "professional docstring for the function. "
        "The docstring MUST follow the 'Google Python Style Guide' for docstrings."
    ),
    expected_output=(
        "A single, ready-formatted docstring text block that can be directly copied into Python code. "
        "The output should contain ONLY the docstring, without additional text before or after."
    ),
    agent=writer_agent,
    context=[analysis_task]  # This task depends on `analysis_task`
)


# --- CREW ASSEMBLY AND EXECUTION ---

# Create the crew with the defined agents and tasks
documentation_crew = Crew(
    agents=[code_analysis_agent, writer_agent],
    tasks=[analysis_task, writing_task],
    process=Process.sequential,  # Tasks are executed one after another
    verbose=True  # Shows the detailed thinking process of the agents
)

# Start the crew's work
if __name__ == "__main__":
    print("Starting MADS Prototype - Cycle 1...")
    print("------------------------------------")
    result = documentation_crew.kickoff()

    print("\n\n------------------------------------")
    print("MADS Prototype - Cycle 1 Complete!")
    print("Generated Docstring:")
    print("------------------------------------")
    print(result)