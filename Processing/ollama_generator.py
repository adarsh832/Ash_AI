import subprocess
import json

class OllamaGenerator:
    def __init__(self, model_name="llama2"):
        self.model = model_name

    def generate_with_context(self, prompt, context=None):
        """Generate response using Ollama with context"""
        try:
            # Format the prompt with context if provided
            if context:
                full_prompt = f"Context: {context}\nPrompt: {prompt}"
            else:
                full_prompt = prompt

            # Call Ollama using subprocess
            cmd = ["ollama", "run", self.model, full_prompt]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error generating response: {result.stderr}"
                
        except Exception as e:
            return f"Failed to generate response: {str(e)}"

    def generate(self, prompt):
        """Simple generation without context"""
        return self.generate_with_context(prompt)