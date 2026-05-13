import ast
import subprocess

def parse_code_constraints(file_paths):
    constraints = {}
    for filepath in file_paths:
        if filepath.endswith('.py'):
            with open(filepath, 'r') as f:
                code = f.read()
                tree = ast.parse(code)
                funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                # Extract simple control flow metrics (e.g., branch counts)
                branches = len([node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While))])
                constraints[filepath] = {"functions": funcs, "branches": branches, "lang": "python"}
                
        elif filepath.endswith('.cpp'):
            # Fallback to C++ minimal parsing (or use clang bindings)
            constraints[filepath] = {"lang": "cpp", "note": "C++ static constraints via CMake/Clang-tidy required"}
            
    return constraints
