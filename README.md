# LangChain AI Code Assistant

This project is an AI-powered code assistant that uses the LangChain framework and the Ollama language model to generate code and answer questions about provided code. The assistant can read code files from the `data` directory using the `code_reader` tool and generate code based on user prompts.

## Features

- Analyzes code and answers questions about provided code
- Generates code based on user prompts
- Uses the `code_reader` tool to read contents of code files in the `data` directory
- Utilizes the LangChain framework and Ollama language model for code generation and analysis
- Provides a Python REPL tool for looking up Python documentation and examples
- Parses the generated code into a JSON object with code, description, and filename
- Saves the generated code to a file in the `output` directory

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/langchain-ai-code-assistant.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Set up the necessary environment variables (e.g., API keys) in a `.env` file.

## Usage

1. Place the code files you want the assistant to analyze in the `data` directory.

2. Run the `main.py` script:

```
python main.py
```

3. Enter a prompt for the AI code assistant. The assistant will generate code, provide a description, and save the code to a file in the `output` directory.

4. To quit the program, enter 'q' when prompted for input.

## Project Structure

- `main.py`: The main script that initializes the LangChain agent, tools, and prompts, and handles user input and output.
- `code_reader.py`: Defines the `CodeReader` tool that reads the contents of code files in the `data` directory.
- `prompts.py`: Contains the prompts used by the LangChain agent and the code parser.
- `data/`: Directory containing code files for the assistant to analyze.
- `output/`: Directory where the generated code files are saved.

## Dependencies

- LangChain
- langchain-community
- dotenv
- ast

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) for providing the framework for building language model-powered applications.
- [Ollama](https://github.com/langchain-community/langchain-community) for the language models used in this project.