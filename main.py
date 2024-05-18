from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import PythonREPL
from agent_tools import code_reader, file_lister
from prompts import code_parser_template, response_classifier_template
from dotenv import load_dotenv
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

llm = Ollama(model="dolphin2.2-mistral:7b-q6_K")
python_repl = PythonREPL()

tools = [
    Tool(
        name="Documentation",
        func=python_repl.run,
        description="For looking up Python documentation and examples of how to use Python libraries/functions."
    ),
    code_reader,
    file_lister
]

custom_tools = [code_reader, file_lister]

agent = initialize_agent(custom_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True)

code_prompt = PromptTemplate(
    input_variables=["response"], 
    template=code_parser_template
)

code_llm = Ollama(model="codellama")

code_chain = LLMChain(llm=llm, prompt=code_prompt)

response_classifier_prompt = PromptTemplate(
    input_variables=["response"],
    template=response_classifier_template
)

response_classifier_chain = LLMChain(llm=code_llm, prompt=response_classifier_prompt)

# Create output directory if it doesn't exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

while (user_input := input("Enter a prompt (or 'q' to quit): ")) != "q":
    if user_input.lower() == "q":
        break

    agent_result = agent({"input": user_input})
    print("Agent result: " + agent_result["output"])
    response_type = response_classifier_chain.run(response=agent_result["output"]).strip().lower()

    if response_type == "code":
        try:
            code_result = code_chain.run(response=agent_result["output"])
            cleaned_json = json.loads(code_result)

            print("Code generated:")
            print(cleaned_json["code"])
            print("\nDescription:", cleaned_json["description"])

            filename = os.path.basename(cleaned_json["filename"])

            file_path = os.path.join(output_dir, filename)
            with open(file_path, "w") as f:
                f.write(cleaned_json["code"])
            print(f"Saved file: {file_path}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing code result: {str(e)}")
        except IOError as e:
            print(f"Error saving file: {str(e)}")
    else:
        print("Conversational response:")
        print(agent_result["output"])