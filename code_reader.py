from langchain.tools import BaseTool
import os

class CodeReader(BaseTool):
    name = "code_reader"
    description = """this tool can read the contents of the project's code files and return 
    their results. Use this when you need to read the contents of the project's code
    
    """
    
    def _run(self, file_name):
        path = os.path.join("data", file_name)
        try:
            with open(path, "r") as f:
                content = f.read()
                return {"file_content": content}
        except Exception as e:
            return {"error": str(e)}
        
    def _arun(self, file_name):
        raise NotImplementedError("CodeReader does not support async")

code_reader = CodeReader()