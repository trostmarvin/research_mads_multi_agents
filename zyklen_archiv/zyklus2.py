# MADS (Multi-Agent Documentation System) - Prototype Cycle 2
# This script extends the prototype to analyze multi-file projects
# and generate diagrams.
# Focus: Collaboration between Navigator, Analyst, Diagram creator, and Writer.

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
# from google.colab import userdata
from dotenv import load_dotenv

# Retrieve the API key from Colab's secrets manager
# os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")

# Load from .env
load_dotenv()

# Check if the key is set
if "OPENAI_API_KEY" not in os.environ:
    print("ERROR: Please set the OPENAI_API_KEY environment variable.")
    exit()

# Select LLM model for agents (e.g. gpt-4o-mini, gpt-4-turbo)
llm = ChatOpenAI(model="gpt-4o-mini")

# --- SIMULATED OPEN-SOURCE PROJECT ---
# Instead of cloning a real repo, we simulate a small project here
# with two files to demonstrate the interaction.
project_files = {
    "main.py": """
from utils import add, subtract

def main():
    \"\"\"Main function of the program.\"\"\"
    a = 10
    b = 5
    print(f"The result of {a} + {b} is {add(a, b)}")
    print(f"The result of {a} - {b} is {subtract(a, b)}")

if __name__ == "__main__":
    main()
""",
    "utils.py": """
def add(x, y):
    \"\"\"Adds two numbers.\"\"\"
    return x + y

def subtract(x, y):
    \"\"\"Subtracts the second number from the first.\"\"\"
    return x - y
"""
}


# --- AGENT DEFINITIONS (Extension for Cycle 2) ---

# 1. NEW: NavigatorAgent - Understands the project structure
navigator_agent = Agent(
    role='Project Architect and Navigator',
    goal='Analyze the structure of a given Python project, identify the individual files, their main tasks, and their dependencies on each other.',
    backstory=(
        "You are an experienced system architect who is able to look at a software project from a bird's eye view. "
        "You immediately recognize how different components work together and create a map of the code that serves as guidance for others."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. CodeAnalysisAgent - Unchanged, analyzes specific code
code_analysis_agent = Agent(
    role='Senior Python Code Analyst',
    goal='Analyze the content of a specific Python file and extract the purpose of the contained functions.',
    backstory=(
        "You are an experienced software developer with a sharp eye for details. "
        "You focus on a single file and break down its logic to provide a detailed function description."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 3. NEW: DiagramAgent - Visualizes the architecture
diagram_agent = Agent(
    role='System Diagram Specialist',
    goal='Create PlantUML component diagram code based on an analysis of the project structure.',
    backstory=(
        "You are a visual thinker and expert in UML and C4 models. You can translate complex system relationships "
        "into simple and clear diagrams. Your preferred language is PlantUML."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)


# 4. WriterAgent - Adapted for creating READMEs
writer_agent = Agent(
    role='Technical Editor for Project Documentation',
    goal='Create a comprehensive and well-structured README.md file for a project. Combine the project structure analysis, detail analysis, and architecture diagram.',
    backstory=(
        "You are a master at combining diverse technical information into coherent and reader-friendly documentation. "
        "You create the final README.md file, which is the flagship of the project."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)


# --- TASK DEFINITIONS (Extension for Cycle 2) ---

# Helper function to present the project as text
def format_project_files(files):
    formatted_string = "Here are the project files:\n\n"
    for filename, content in files.items():
        formatted_string += f"--- File: {filename} ---\n"
        formatted_string += f"```python\n{content}\n```\n\n"
    return formatted_string

# Task 1: Analyze project structure (NavigatorAgent)
navigation_task = Task(
    description=f"Analyze the following collection of Python files:\n\n{format_project_files(project_files)}\n\n"
                "Describe the purpose of each file and how they depend on each other (e.g., which file imports functions from another).",
    expected_output="A clear text summary that describes each file and its role in the project as well as the import relationships.",
    agent=navigator_agent
)

# Task 2: Create diagram (DiagramAgent)
# This task uses the output from navigation_task
diagram_task = Task(
    description="Based on the provided project structure analysis, create the code for a simple PlantUML component diagram. "
                "The diagram should represent the files as components and the imports as relationships.",
    expected_output="A single code block with valid PlantUML syntax that begins with @startuml and ends with @enduml.",
    agent=diagram_agent,
    context=[navigation_task]
)

# Task 3: Write final README.md (WriterAgent)
# This task uses the outputs from the previous tasks
writing_task = Task(
    description="Create a complete README.md file for the project. Use the project overview and PlantUML code that are provided to you. "
                "The README file should have the following sections:\n"
                "1. ## Project Overview (based on the structure analysis)\n"
                "2. ## Architecture (contains the PlantUML code in a 'plantuml' code block)\n"
                "3. ## Components (a brief description of each file)",
    expected_output="A fully formatted Markdown file (README.md) that contains all requested information in a clear structure.",
    agent=writer_agent,
    context=[navigation_task, diagram_task]
)


# --- CREW ASSEMBLY AND EXECUTION ---
project_documentation_crew = Crew(
    agents=[navigator_agent, diagram_agent, writer_agent],
    tasks=[navigation_task, diagram_task, writing_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("Starting MADS Prototype - Cycle 2...")
    print("------------------------------------")
    result = project_documentation_crew.kickoff()

    print("\n\n------------------------------------")
    print("MADS Prototype - Cycle 2 Complete!")
    print("Generated README.md:")
    print("------------------------------------")
    print(result)
