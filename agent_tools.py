from langchain.tools import BaseTool
import os
import re

class CodeReader(BaseTool):
    name = "code_reader"
    description = """
    This tool reads the contents of a code file from the 'project' directory and returns the file content.
    Use this tool when you need to examine the code in a specific file.
    Provide the filename as input, e.g., 'example.py'.
    """
    
    def _run(self, file_name):
        file_name = file_name.strip("'")

        path = os.path.join("project", file_name)
        try:
            with open(path, "r") as f:
                content = f.read()
                return {"file_content": content}
        except FileNotFoundError:
            raise ValueError(f"File '{file_name}' not found in the 'project' directory.")
        except Exception as e:
            raise ValueError(f"Error reading file '{file_name}': {str(e)}")

code_reader = CodeReader()

class FileLister(BaseTool):
    name = "file_lister"
    description = """
    This tool lists the files in a specified directory. If no directory is provided, it defaults to the 'project' directory.
    Use this tool when you need to know the available files in a specific directory.
    Optionally provide the directory path as input, e.g., 'data'. If no input is provided, it will list files in the 'project' directory.
    """
    def _run(self, directory: str = "") -> dict:
        # Extract the directory path from the input string
        match = re.search(r"'(.*?)'", directory)
        if match:
            data_dir = match.group(1)
        else:
            data_dir = directory.strip() or "project"
        
        if not os.path.isdir(data_dir):
            raise ValueError(f"Directory '{data_dir}' does not exist.")
        files = os.listdir(data_dir)
        return {"files": files}

    def _arun(self, dummy_input: str = "") -> dict:
        raise NotImplementedError("FileLister does not support async")

file_lister = FileLister()