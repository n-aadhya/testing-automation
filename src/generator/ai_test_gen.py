import os
import openai

def load_context(folder_path):
    # Load RTM and PCM markdown/text files
    context = ""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            with open(os.path.join(folder_path, file), 'r') as f:
                context += f.read() + "\n"
    return context

def generate_tests(constraints, rtm_path, pcm_path):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    rtm_context = load_context(rtm_path)
    pcm_context = load_context(pcm_path)
    
    generated_test_files =[]
    
    for filepath, details in constraints.items():
        if details['lang'] == "python":
            prompt = f"""
            You are an autonomous testing AI. Write robust Pytest unit tests for the functions: {details['functions']} in {filepath}.
            Ensure tests satisfy these Protocol Contexts: {pcm_context}
            Ensure tests trace back to these Requirements: {rtm_context}
            Output only the raw Python test code. Include edge cases for {details['branches']} branches.
            """
            
            # Using GPT-4 for safe, intelligent test case creation
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}]
            )
            
            test_code = response.choices[0].message['content']
            
            # Save the adaptive test
            test_filename = f"tests/test_{os.path.basename(filepath)}"
            with open(test_filename, "w") as f:
                f.write(test_code)
                
            generated_test_files.append(test_filename)
            
    return generated_test_files
