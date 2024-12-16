import os
import re
from dotenv import load_dotenv
from swarms import Agent, AgentRearrange
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize Groq client
client = Groq(api_key=api_key)
print("Environment set up and Groq client initialized successfully!")

# Define the Groq-based model
class GroqModel:
    def __init__(self, client):
        self.client = client

    def __call__(self, prompt):
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Python code expert."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during API call: {e}")
            return f"Error: {e}"

# Initialize the model
model = GroqModel(client=client)

# Define agents
first_draft_agent = Agent(
    agent_name="First Draft Writer",
    system_prompt="""
    You are a Python software engineer specializing in creating high-quality first drafts of Python programs. Given a
    functional requirement or user-provided input, design a Python program that is logically structured, adheres to PEP 8
    standards, and includes the following:
    
    1. Clear function definitions and modular code organization.
    2. Inline comments that explain the purpose of each function and critical sections of the code.
    3. Basic test cases, if applicable, to demonstrate functionality.
    4. Efficient use of Python's standard libraries.

    Your goal is to produce a well-structured, initial version of the program that other agents can refine further.
    """,
    llm=model,
    max_loops=1,
)

compatibility_agent = Agent(
    agent_name="Framework Compatibility Reviewer",
    system_prompt="""
    You are a Python expert with deep knowledge of machine learning (ML) and AI inference frameworks, agent-based
    programming libraries, and AI application layers. Review the provided Python program draft and perform the following tasks:
    
    1. Identify potential compatibility issues with popular ML/AI frameworks (e.g., TensorFlow, PyTorch, scikit-learn).
    2. Suggest improvements for library imports, ensuring optimal usage of relevant frameworks.
    3. Evaluate whether the code adheres to best practices for integrating AI/ML workflows and agent-based systems.
    4. Recommend any changes to ensure the program can function correctly and efficiently in modern AI environments.

    Your feedback should include the corrected and improved version of the code, with explanations for the changes made.
    """,
    llm=model,
    max_loops=1,
)

qa_agent = Agent(
    agent_name="Functional QA and Integration Advisor",
    system_prompt="""
    You are a Python quality assurance expert and software architect. Your task is to assess the provided Python program for
    its functional requirements, interoperability, and overall quality. Specifically, you should:
    
    1. Ensure that the code meets the stated functional requirements and identify any gaps or ambiguities.
    2. Evaluate the program's potential for integration with other software modules and suggest the next logical program
       or feature that could complement this one.
    3. Perform a debugging analysis to identify any runtime issues or logical errors.
    4. Suggest general improvements to enhance code quality, maintainability, and scalability.

    Your output should include the finalized and polished version of the program, along with a brief explanation of its
    suitability for deployment and interoperability with other modules.
    """,
    llm=model,
    max_loops=1,
)

# Define flow and swarm system
agents = [first_draft_agent, compatibility_agent, qa_agent]
flow = f"{first_draft_agent.agent_name} -> {compatibility_agent.agent_name} -> {qa_agent.agent_name}"

code_refinement_system = AgentRearrange(
    name="PythonCodeRefinementSystem",
    description="Swarm system for generating, refining, and assessing Python programs",
    agents=agents,
    flow=flow,
    max_loops=1,
    output_type="all",
)

# Helper function to save the final output to a .py file
def save_to_py_file(filename, code):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(code)
    print(f"Finalized code saved to {filename}")

# Main processing function
def process_code(input_prompt, output_filename):
    try:
        # Step through the agents
        draft_code = first_draft_agent(input_prompt)
        refined_code = compatibility_agent(draft_code)
        final_code = qa_agent(refined_code)

        # Save the final output to a .py file
        save_to_py_file(output_filename, final_code)

        print("Code refinement process completed successfully!")
    except Exception as e:
        print(f"Error during code processing: {e}")

if __name__ == "__main__":
    # Example input prompt
    input_prompt = """
    Create a Python program that loads a dataset, preprocesses it by normalizing numeric values, and splits it into training
    and test sets. The program should be modular, use standard Python libraries, and demonstrate basic functionality.
    """

    output_file = "refined_program.py"
    process_code(input_prompt, output_file)
