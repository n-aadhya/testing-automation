import os
from openai import OpenAI

def load_context(folder_path):
    # Load RTM and PCM markdown/text files
    context = ""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    context += f.read() + "\n"
    return context

def generate_tests(constraints, rtm_path, pcm_path):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return[]
        
    # 1. ADD base_url FOR OPENROUTER
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    
    rtm_context = load_context(rtm_path)
    pcm_context = load_context(pcm_path)
    
    generated_test_files =[]
    os.makedirs("tests", exist_ok=True)
    
    for filepath, details in constraints.items():
        if details.get('lang') == "python":
            prompt = f"""
            You are an autonomous testing AI. Write robust Pytest unit tests for the functions: {details.get('functions')} in {filepath}.
            Ensure tests satisfy these Protocol Contexts: {pcm_context}
            Ensure tests trace back to these Requirements: {rtm_context}
            Output ONLY the raw Python test code. Do not include markdown blocks like ```python. Include edge cases for {details.get('branches')} branches.
            """
            
            print(f"Generating tests for {filepath} using free OpenRouter model...")
            
            # 2. CHANGE MODEL TO A FREE OPENROUTER MODEL
            response = client.chat.completions.create(
                model="openrouter/free", 
                messages=[{"role": "user", "content": prompt}]
            )
            
            test_code = response.choices[0].message.content
            test_code = test_code.replace("```python\n", "").replace("```python", "").replace("```", "").strip()
            
            test_filename = f"tests/test_{os.path.basename(filepath)}"
            with open(test_filename, "w", encoding='utf-8') as f:
                f.write(test_code)
                
            generated_test_files.append(test_filename)
            
    return generated_test_files
