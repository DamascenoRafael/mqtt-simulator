import math

ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}

def evaluate(expression):
    lambda_expression = "lambda x: "+expression
    code = compile(lambda_expression, "<string>", "eval")

    for name in code.co_names:
        if name not in ALLOWED_NAMES:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {},"math":math}, ALLOWED_NAMES)
