# MADS (Multi-Agent Documentation System) - Enhanced Version
# Optimized for better documentation generation without UML support

import os
import json
from typing import Dict, List
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai.tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLMs with optimized temperatures
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
analyzer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)  # Lower temp for analysis

# --- ENHANCED TOOLS ---

class FileWriteTool(BaseTool):
    name: str = "File Writer"
    description: str = "Writes given text content to a specified file with proper formatting."

    def _run(self, file_path: str, content: str) -> str:
        """
        Writes content to a specified file with error handling.
        """
        try:
            output_dir = os.path.dirname(file_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File '{file_path}' successfully written with {len(content)} characters."
        except IOError as e:
            return f"Error writing file '{file_path}': {e}"

class CodeAnalyzerTool(BaseTool):
    name: str = "Code Analyzer"
    description: str = "Analyzes code files to extract functions, classes, dependencies, and patterns."
    
    def _run(self, file_path: str) -> str:
        """
        Performs basic code analysis on a file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            lines = content.split('\n')
            analysis = {
                "file": file_path,
                "lines": len(lines),
                "has_classes": 'class ' in content,
                "has_functions": 'def ' in content or 'function ' in content,
                "imports": [l.strip() for l in lines if l.strip().startswith(('import ', 'from ', 'require', 'include'))],
                "file_type": os.path.splitext(file_path)[1]
            }
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing {file_path}: {e}"

# Instantiate tools
directory_tool = DirectoryReadTool()
file_tool = FileReadTool()
file_write_tool = FileWriteTool()
code_analyzer_tool = CodeAnalyzerTool()

# --- ENHANCED AGENT DEFINITIONS ---

# 1. Project Navigator - Enhanced with better exploration strategy
navigator_agent = Agent(
    role='Senior Project Navigator',
    goal='Create a comprehensive map of the project structure, identifying all files, directories, and their relationships.',
    backstory="""You are an experienced code explorer with 10+ years analyzing codebases. 
    You excel at understanding project layouts, identifying entry points, configuration files, 
    and creating clear mental models of how projects are organized. You always provide 
    structured, hierarchical views of project directories.""",
    verbose=True,
    allow_delegation=False,
    tools=[directory_tool, file_tool],
    llm=llm,
    max_iter=5
)

# 2. Code Analyzer - New agent for deeper code understanding
code_analyzer_agent = Agent(
    role='Code Analysis Specialist',
    goal='Analyze code files to understand functionality, dependencies, patterns, and architecture.',
    backstory="""You are a senior software architect who specializes in reverse-engineering codebases. 
    You can identify design patterns, understand dependencies, detect code smells, and explain 
    complex logic in simple terms. You focus on understanding the 'why' behind code structures.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_tool, code_analyzer_tool],
    llm=analyzer_llm,
    max_iter=5
)

# 3. Technical Writer - Enhanced with better documentation skills
writer_agent = Agent(
    role='Senior Technical Documentation Expert',
    goal='Create comprehensive, well-structured README.md documentation that is both informative and easy to understand.',
    backstory="""You are a technical writer with expertise in creating developer documentation. 
    You know how to structure README files with proper sections including: Project Overview, 
    Features, Installation, Usage, Project Structure, Configuration, API Documentation, 
    Contributing Guidelines, and License. You use markdown effectively with code blocks, 
    tables, and clear formatting. You always ensure documentation is actionable and helpful.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_write_tool],
    llm=llm,
    max_iter=3
)

# 4. Documentation Reviewer - New agent for quality assurance
reviewer_agent = Agent(
    role='Documentation Quality Reviewer',
    goal='Review and enhance documentation for completeness, clarity, and technical accuracy.',
    backstory="""You are a senior developer who reviews documentation for open-source projects. 
    You ensure documentation is complete, accurate, follows best practices, and includes 
    all necessary sections. You check for missing information, unclear explanations, 
    and suggest improvements for better developer experience.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_tool, file_write_tool],
    llm=llm,
    max_iter=2
)

# --- ENHANCED TASK DEFINITIONS ---

# Task 1: Project Structure Analysis
structure_analysis_task = Task(
    description="""Analyze the complete structure of the project in directory '{project_directory}':
    1. List all directories and subdirectories with their purposes
    2. Identify all file types present (e.g., .py, .js, .json, .md)
    3. Locate key files (README, configuration files, main entry points)
    4. Create a hierarchical tree view of the project structure
    5. Identify the technology stack based on file extensions and config files""",
    expected_output="""A detailed project structure report including:
    - Hierarchical directory tree
    - List of all files grouped by type
    - Identified technology stack
    - Key configuration files
    - Entry points and main modules""",
    agent=navigator_agent
)

# Task 2: Code Analysis
code_analysis_task = Task(
    description="""Based on the project structure, analyze the codebase in '{project_directory}':
    1. Examine main code files to understand functionality
    2. Identify key classes, functions, and modules
    3. Map dependencies and imports
    4. Detect design patterns and architectural decisions
    5. Note any external libraries or frameworks used
    6. Identify API endpoints if applicable""",
    expected_output="""A comprehensive code analysis report including:
    - Main functionalities and features
    - Key components and their responsibilities
    - Dependency graph
    - Used design patterns
    - External dependencies list
    - API documentation if applicable""",
    agent=code_analyzer_agent,
    context=[structure_analysis_task]
)

# Task 3: Documentation Creation
documentation_task = Task(
    description="""Create a professional README.md for the project in '{project_directory}':
    Use the structure and code analysis to write comprehensive documentation including:
    1. Project title and description
    2. Features and capabilities
    3. Prerequisites and requirements
    4. Installation instructions
    5. Usage examples with code snippets
    6. Project structure explanation
    7. Configuration guide
    8. API documentation (if applicable)
    9. Contributing guidelines
    10. License information
    
    Save the README.md in the project root directory.""",
    expected_output="A complete, well-formatted README.md file saved in the project directory",
    agent=writer_agent,
    context=[structure_analysis_task, code_analysis_task]
)

# Task 4: Documentation Review and Enhancement
review_task = Task(
    description="""Review and enhance the generated README.md in '{project_directory}':
    1. Check for completeness of all sections
    2. Verify technical accuracy
    3. Ensure clarity and readability
    4. Add missing information if needed
    5. Format code examples properly
    6. Add badges if applicable (version, license, etc.)
    7. Ensure links and references are correct
    8. Update the file with improvements""",
    expected_output="An enhanced, production-ready README.md with all improvements applied",
    agent=reviewer_agent,
    context=[documentation_task]
)

# --- OPTIMIZED CREW ASSEMBLY ---
documentation_crew = Crew(
    agents=[navigator_agent, code_analyzer_agent, writer_agent, reviewer_agent],
    tasks=[structure_analysis_task, code_analysis_task, documentation_task, review_task],
    process=Process.sequential,
    verbose=True,
    memory=True,  # Enable memory for better context retention
    full_output=True  # Get complete output from all agents
)

# --- ENHANCED EXECUTION ---
if __name__ == "__main__":
    # Configuration
    PROJECT_DIR = os.getenv("PROJECT_DIR", "test_project")
    
    # Validate project directory
    if not os.path.exists(PROJECT_DIR):
        print(f"ERROR: Directory '{PROJECT_DIR}' not found!")
        print("Please set PROJECT_DIR environment variable or ensure 'test_project' exists.")
        exit(1)
    
    print(f"✓ Target directory '{PROJECT_DIR}' found.")
    print(f"  Files found: {len(os.listdir(PROJECT_DIR))}")
    
    print("\n" + "="*50)
    print("Starting MADS - Enhanced Documentation System")
    print("="*50 + "\n")
    
    try:
        # Execute the crew with error handling
        result = documentation_crew.kickoff(
            inputs={"project_directory": PROJECT_DIR}
        )
        
        print("\n" + "="*50)
        print("✓ Documentation Generation Complete!")
        print("="*50)
        
        # Check if README was created
        readme_path = os.path.join(PROJECT_DIR, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                lines = f.readlines()
            print(f"✓ README.md created successfully ({len(lines)} lines)")
            print(f"✓ Location: {readme_path}")
        else:
            print("⚠ README.md not found in expected location")
            
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Please check your configuration and try again.")
