response_classifier_template = """
Please classify the following response as either "code" or "conversation":

{response}

Reply with only "code" or "conversation".
"""

code_parser_template = """
Please parse the response from the previous LLM into a JSON object with the following structure:

{{
    "code": "<code_string>",
    "description": "<description_string>",
    "filename": "<filename_string>"
}}

- Replace <code_string> with the generated code.
- Replace <description_string> with a brief description of what the code does.
- Replace <filename_string> with a valid filename (without special characters) for saving the code.

Example:
{{
    "code": "def add(a, b):\\n    return a + b",
    "description": "A function that adds two numbers",
    "filename": "add_numbers.py"
}}

Here is the response to parse: {response}
"""
