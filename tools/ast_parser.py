import ast
import re

def extract_cpp_conditions(file_path):
    conditions = []

    with open(file_path, "r") as f:
        code = f.read()

    matches = re.findall(r'if\s*\((.*?)\)', code)

    for m in matches:
        conditions.append(m)

    return conditions


class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.conditions = []

    def visit_If(self, node):
        self.conditions.append(ast.unparse(node.test))
        self.generic_visit(node)


def extract_conditions(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    extractor = ConditionExtractor()
    extractor.visit(tree)

    return extractor.conditions
