import os
import json
from dotenv import load_dotenv
from swarms import Agent, AgentRearrange
from groq import Groq
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize Groq client
client = Groq(api_key=api_key)

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
            return f"Error: {e}"

# Initialize the model
model = GroqModel(client=client)

# Define agents with updated system prompts
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
    You are a Python expert with deep knowledge of machine learning (ML) and AI frameworks, agent-based programming libraries,
    and AI application layers. Given the provided Python code (either user input or generated by the first draft agent), perform the following tasks:

    1. **Framework and Library Compatibility**:
        - Identify the libraries and frameworks used in the code. If no specific libraries are provided, suggest the most appropriate ones based on the functionality described in the prompt.
        - If the code uses a particular framework, evaluate its structure and ensure it follows best practices for that framework. Avoid making assumptions about other frameworks.
        
    2. **Propose Integration Scenarios**:
        - Suggest how the provided code could integrate with other tools or platforms (e.g., web frameworks, cloud platforms, data processing tools). This should be based on the user’s request.
        
    3. **File Structure Recommendations**:
        - Based on the provided code or prompt, suggest the most suitable file structure for a project repository, considering modularization and scalability.
        - Do not assume a generic structure, but propose one that fits the specific use case described by the user.
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

# Function to process user input through the agent system
def process_prompt(prompt):
    try:
        # First draft
        draft_code = first_draft_agent(prompt)
        
        # Compatibility review and framework suggestions
        refined_code = compatibility_agent(draft_code)
        
        # Final code after QA
        final_code = qa_agent(refined_code)
        
        return final_code
    except Exception as e:
        return f"Error: {e}"

# Gradio interface
conversation_history = []
is_first_launch = True  # Flag to indicate first launch

def chat_ui(user_input, chat_history):
    global conversation_history, is_first_launch

    # Process input through agent system
    ai_response = process_prompt(user_input)

    # Update conversation history
    chat_history.append(("User", user_input))
    chat_history.append(("AI", ai_response))
    conversation_history.append({"user": user_input, "ai": ai_response})

    # Only trigger sharing on the first launch
    share_flag = is_first_launch
    if is_first_launch:
        is_first_launch = False

    return chat_history, share_flag

def save_conversation():
    global conversation_history
    file_path = "conversation_history.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, indent=4)
    return f"Conversation saved to {file_path}"

# Gradio Layout with gr.Row() and gr.Column()
with gr.Blocks() as demo:
    with gr.Row():
        chat_history = gr.Chatbot(label="Python Code Refinement Chat", elem_id="chatbox", height=600)
    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Enter your Python code prompt here...", 
            lines=6,  # Increased from 3 to 6 to make it larger
            max_lines=10,  # Increased max lines 
            elem_id="code-input"
        )
    with gr.Row():
        copy_button = gr.Button("Copy Response to Clipboard")
        save_button = gr.Button("Save Conversation to JSON")
        submit_button = gr.Button("Submit")
    
    # Add CSS to control input height and appearance
    demo.css = """
    #code-input {
        min-height: 150px !important;
    }
    """
    
    submit_button.click(
        chat_ui, 
        inputs=[user_input, chat_history], 
        outputs=[chat_history, gr.Textbox(visible=False)]  # Corrected output here
    )
    
    # Copy last AI response to clipboard
    copy_button.click(
        lambda: chat_history.value[-1]['text'] if chat_history.value else "", 
        outputs=None
    )
    
    save_button.click(save_conversation, outputs=gr.Textbox(visible=False))

    # Trigger submit when Enter key is pressed in the input field
    user_input.submit(
        chat_ui, 
        inputs=[user_input, chat_history], 
        outputs=[chat_history, gr.Textbox(visible=False)]  # Corrected output here
    )

    # Launch with share flag set only on the first launch
    demo.launch(share=True if is_first_launch else False)