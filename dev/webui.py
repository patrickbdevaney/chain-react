import gradio as gr
from pathlib import Path
import pyperclip

# Initial state for toggles (enabled by default)
memory_enabled = True
rag_enabled = True
web_search_enabled = True
agents_enabled = True

# Function to handle toggles
def toggle_memory():
    global memory_enabled
    memory_enabled = not memory_enabled
    return f"Memory Enabled: {memory_enabled}"

def toggle_rag():
    global rag_enabled
    rag_enabled = not rag_enabled
    return f"RAG Enabled: {rag_enabled}"

def toggle_web_search():
    global web_search_enabled
    web_search_enabled = not web_search_enabled
    return f"Web Search Enabled: {web_search_enabled}"

def toggle_agents():
    global agents_enabled
    agents_enabled = not agents_enabled
    return f"Agents Enabled: {agents_enabled}"

# Dummy backend function with all components considered
def process_prompt(prompt):
    response = f"Processing: '{prompt}'\n"
    
    if memory_enabled:
        response += "Using Conversational Memory...\n"
    if rag_enabled:
        response += "Retrieving from RAG...\n"
    if web_search_enabled:
        response += "Searching the Web...\n"
    if agents_enabled:
        response += "Using Agents for Sequential Processing...\n"
    
    # Simulated response for testing
    response += f"Final Answer for '{prompt}'"
    
    return response

# Copy text to clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)
    return "Copied to clipboard!"

# Gradio UI
def create_ui():
    with gr.Blocks() as ui:
        # Conversation history area
        conversation_history = gr.Textbox(
            lines=15, label="Conversation", interactive=False, show_label=False
        )
        
        # Input box for user prompts
        input_box = gr.Textbox(lines=1, placeholder="Type your message here...", show_label=False)
        
        # Buttons for toggling different components
        copy_button = gr.Button("Copy Last Response")
        memory_toggle = gr.Button("Toggle Memory (Default: Enabled)")
        rag_toggle = gr.Button("Toggle RAG (Default: Enabled)")
        web_search_toggle = gr.Button("Toggle Web Search (Default: Enabled)")
        agents_toggle = gr.Button("Toggle Agents (Default: Enabled)")
        clear_button = gr.Button("Clear Conversation")
        
        # Event Handlers
        def handle_input(user_input, history):
            response = process_prompt(user_input)
            updated_history = history + f"User: {user_input}\nLLM: {response}\n\n"
            return updated_history, response

        input_box.submit(
            handle_input, [input_box, conversation_history], [conversation_history, None]
        )
        
        # Copy last response to clipboard
        copy_button.click(
            lambda history: copy_to_clipboard(history.split("LLM:")[-1].strip()),
            [conversation_history],
            None,
        )
        
        # Toggle event handlers
        memory_toggle.click(toggle_memory, None, [conversation_history])
        rag_toggle.click(toggle_rag, None, [conversation_history])
        web_search_toggle.click(toggle_web_search, None, [conversation_history])
        agents_toggle.click(toggle_agents, None, [conversation_history])
        
        # Clear conversation history
        clear_button.click(lambda: "", None, conversation_history)

    return ui


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()