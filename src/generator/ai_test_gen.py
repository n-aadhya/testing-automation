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
        lang = details.get('lang')
        
        if lang == "python":
            framework = "Pytest"
            file_ext = ".py"
        elif lang == "cpp":
            framework = "GTest (Google Test) in C++"
            file_ext = ".cpp"
        else:
            continue

        prompt = f"""
        You are an autonomous testing AI. Write robust {framework} unit tests for the functions: {details.get('functions', 'the code')} in {filepath}.
        Ensure tests satisfy these Protocol Contexts: {pcm_context}
        Ensure tests trace back to these Requirements: {rtm_context}
        Output ONLY the raw {lang} test code. Do not include markdown blocks.
        """
        
        print(f"Generating {framework} tests for {filepath}...")
        
        # Using the OpenRouter auto-free model we set up earlier
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        
        test_code = response.choices[0].message.content
        # Clean markdown wrappers
        test_code = test_code.replace(f"```{lang}\n", "").replace("```", "").strip()
        
        # Save the test with the correct extension
        test_filename = f"tests/test_{os.path.basename(filepath).split('.')[0]}{file_ext}"
        with open(test_filename, "w", encoding='utf-8') as f:
            f.write(test_code)
            
        generated_test_files.append(test_filename)
    return generated_test_files
