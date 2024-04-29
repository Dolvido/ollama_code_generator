from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import PythonREPL
from code_reader import code_reader
from prompts import agent_context, code_parser_template
from dotenv import load_dotenv
import os
import ast

llm = Ollama(model="mistral")
python_repl = PythonREPL()

tools = [
    Tool(
        name = "Documentation",
        func=python_repl.run,
        description="For looking up Python documentation and examples of how to use Python libraries/functions."
    ),
    code_reader,
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True)

code_prompt = PromptTemplate(
    input_variables=["response"], 
    template=code_parser_template
)

code_llm = Ollama(model="codellama")

code_chain = LLMChain(llm=llm, prompt=code_prompt)

while (user_input := input("Enter a prompt (or 'q' to quit): ")) != "q":
    if user_input.lower() == "q":
        break
    
    agent_result = agent.run(user_input)
    #agent_result = agent({"input":user_input})
    code_result = code_chain.run(response=agent_result)

    cleaned_json = ast.literal_eval(code_result)
    
    print("Code generated:")
    print(cleaned_json["code"])
    print("\nDescription:", cleaned_json["description"])

    filename = cleaned_json["filename"]

    try:
        with open(os.path.join("output", filename), "w") as f:
            f.write(cleaned_json["code"])
        print("Saved file", filename)
    except:
        print("Error saving file...")