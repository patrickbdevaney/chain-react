# Chain-React: A Sequential Agent Gradio Chat Interface
## Overview
**Chain-React** is a Python-based chatbot powered by a sequential chain of agents, utilizing the Groq API and a variety of agent-based tasks to refine and optimize Python code based on user inputs. The system allows users to interact with different agents in a chat interface, guiding the process of writing, reviewing, and testing Python code through multiple stages.

## Features
* **Sequential Agents**: The interface uses a chain of agents, each responsible for a specific task in the code generation and review process:
  1. **First Draft Writer**: Generates the first draft of a Python program based on the user's input.
  2. **Framework Compatibility Reviewer**: Reviews the generated code for compatibility with various frameworks, suggesting improvements and integrations.
  3. **QA and Integration Advisor**: Assesses the quality, functionality, and integration potential of the generated code, providing feedback and final refinements.
* **Groq Integration**: Utilizes the Groq API for natural language processing, enabling the agents to communicate with each other and generate meaningful Python code based on user input.
* **Gradio Interface**: A user-friendly web interface that allows users to input their code requirements, interact with the agents, and receive the refined Python code.
* **Conversation History**: All user interactions are saved in a conversation history file (`conversation_history.json`), allowing users to review previous exchanges and continue working on prior discussions.

## Project Structure
```markdown
chain-react/
│
├── app.py # Main application file containing the Gradio interface and agent interactions.
├── .env # Environment variables file for storing API keys and configurations.
├── conversation_history.json # Stores the conversation history between the user and agents.
└── README.md # This file.
```

## Installation
### Requirements
* Python 3.8+
* Groq API Key (create an account at [Groq](https://www.groq.com/) and generate an API key)
* Required Python packages (listed in `requirements.txt`)

### Steps to Install
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/chain-react.git
   cd chain-react
   ```
2. Install dependencies:
   It is recommended to set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For macOS/Linux
   venv\Scripts\activate      # For Windows
   ```
   Then install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Create a `.env` file in the root of the project directory and add your Groq API key:
   ```makefile
   GROQ_API_KEY=your_api_key_here
   ```
4. Run the application:
   To start the Gradio interface and begin interacting with the agents, run:
   ```bash
   python app.py
   ```
   The application will launch a local Gradio interface, which you can access in your web browser.

## Usage
### Gradio Interface
Once the application is running, navigate to the provided local URL (e.g., http://127.0.0.1:7860/), and you’ll see the following components:
* **Chatbox**: This area displays the conversation history between the user and the agents. It shows both user input and the agent responses.
* **User Input**: A textbox where the user can input a Python code prompt or ask for code-related assistance. The input is processed and passed through the agent chain for refinement.
* **Submit Button**: Triggers the submission of the user input. This button can be clicked or pressed via the Enter key.
* **Copy Response to Clipboard**: A button that copies the most recent AI response to the clipboard for easy use.
* **Save Conversation**: A button that allows users to save the entire conversation history into a `conversation_history.json` file.

### How it Works
1. **User Input**: The user enters a Python code prompt, such as "Write a Python function that adds two numbers."
2. **Agent 1 - First Draft Writer**: The system generates an initial Python program based on the user's prompt.
3. **Agent 2 - Compatibility Reviewer**: The code is reviewed for compatibility with Python libraries and frameworks. The agent suggests optimizations or changes.
4. **Agent 3 - QA and Integration Advisor**: The code is tested for logical errors, functional issues, and integration potential. The agent provides feedback on quality and suggests improvements.
The output is then displayed back to the user in the chat interface.

### Example Interaction
User: Write a Python function to fetch weather data from an API.
Agent 1: Generates the first draft of the function using basic Python libraries.
Agent 2: Reviews the function for compatibility with popular web frameworks like requests.
Agent 3: Suggests optimizations for error handling and code quality.
The conversation history is saved and can be revisited later for improvements or further discussion.

### Saving Conversations
Conversations are stored in a `conversation_history.json` file for easy review. This is useful for tracking progress, debugging issues, or continuing work on previous interactions.
```json
[
  {
    "user": "Write a Python function to fetch weather data from an API.",
    "ai": "Here’s a function that uses the `requests` library to fetch weather data..."
  }
]
```

## Agents Overview
1. **First Draft Writer**:
   * Role: Generates the first draft of Python code based on user-provided prompts.
   * System Prompt: The agent generates modular, well-commented Python code adhering to PEP 8 standards.
2. **Framework Compatibility Reviewer**:
   * Role: Reviews the generated code to ensure compatibility with various Python libraries and frameworks.
   * System Prompt: This agent identifies used libraries, suggests framework-specific improvements, and provides integration ideas.
3. **QA and Integration Advisor**:
   * Role: Evaluates the final code for quality, functional requirements, and potential integration with other software modules.
   * System Prompt: The agent checks for errors, proposes optimizations, and ensures the code is ready for deployment.

## Troubleshooting
1. **API Key Issues**:
   If you encounter errors related to the Groq API, double-check that your API key is correctly set in the `.env` file.
2. **Gradio Interface Not Launching**:
   Ensure all dependencies are installed and your virtual environment is activated. If issues persist, check for errors in the terminal and ensure no other processes are using the port.
3. **Conversation History Not Saving**:
   If the `conversation_history.json` file is not being created, check for write permissions in the directory and ensure the program has proper access to create the file.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
* Groq for providing the API used in the system.
* Gradio for the powerful and easy-to-use interface for machine learning models.
