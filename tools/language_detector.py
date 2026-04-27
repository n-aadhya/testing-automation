import os

def detect_language(file_path):
    _, ext = os.path.splitext(file_path)

    if ext in [".c", ".cpp", ".h", ".hpp"]:
        return "cpp"
    elif ext == ".py":
        return "python"
    else:
        return "unknown"
