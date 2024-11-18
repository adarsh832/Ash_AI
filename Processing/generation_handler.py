import subprocess
import json
from typing import Optional, Dict, List

class GenerationHandler:
    def __init__(self):
        """
        Initialize the generation handler with llama3.2 model
        """
        self.model = "llama3.2"
        self.context_history = []
        self.max_context_length = 5

    def generate_response(self, query: str, context: Optional[Dict] = None) -> str:
        """Generate a response for the given query using llama3.2"""
        try:
            # Add context to history
            if context:
                self.context_history.append({"query": query, "context": context})
                if len(self.context_history) > self.max_context_length:
                    self.context_history.pop(0)

            prompt = self._format_prompt(query)
            cmd = ["ollama", "run", "llama3.2", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return self._format_response(result.stdout.strip())
            else:
                return f"Error generating response: {result.stderr}"

        except Exception as e:
            return f"Failed to generate response: {str(e)}"

    def _format_prompt(self, query: str) -> str:
        """Format the prompt with context history and system instructions"""
        prompt = (
            "<<SYS>>\n"
            "You are Ash, an advanced AI assistant created by Adarsh Shah. Follow these guidelines:\n"
            "1. Keep responses concise and direct by default\n"
            "2. Use a confident, professional tone with a touch of personality\n"
            "3. Address the user as 'Sir' occasionally\n"
            "4. Response style:\n"
            "   - Default: Short, clear answers\n"
            "   - Only provide detailed explanations when specifically asked\n"
            "   - Use technical terms only when relevant\n"
            "   - Add subtle wit when appropriate\n"
            "5. When handling technical tasks:\n"
            "   - Confirm actions before execution\n"
            "   - Provide status updates\n"
            "   - Prioritize efficiency and security\n"
            "<</SYS>>\n\n"
        )

        if self.context_history:
            prompt += "Previous context:\n"
            for item in self.context_history:
                prompt += f"Human: {item['query']}\n"
                if item['context']:
                    prompt += f"Context: {json.dumps(item['context'])}\n"
            prompt += "\n"

        prompt += f"Human: {query}\n\nAssistant: "
        return prompt

    def _format_response(self, response: str) -> str:
        """Format the response for better readability"""
        # Remove any system or formatting artifacts
        response = response.replace("<<SYS>>", "").replace("<</SYS>>", "")
        lines = response.split('\n')
        cleaned_lines = [
            line.strip() for line in lines 
            if not line.strip().startswith(('Human:', 'Assistant:', 'System:'))
            and line.strip()
        ]
        return '\n'.join(cleaned_lines)

    def handle_specific_queries(self, query_type: str, query: str) -> str:
        """Handle specific types of queries"""
        prompts = {
            'code': (
                "Write code for this request. Include:\n"
                "1. Implementation\n"
                "2. Comments explaining the code\n"
                "3. Example usage\n"
            ),
            'explanation': (
                "Explain this concept. Include:\n"
                "1. Simple explanation\n"
                "2. Key points\n"
                "3. Examples if relevant\n"
            ),
            'general': "Provide a clear and helpful response to this query:\n"
        }

        prompt_prefix = prompts.get(query_type, prompts['general'])
        formatted_query = f"{prompt_prefix}{query}"
        return self.generate_response(formatted_query)

    def clear_context(self):
        """Clear the context history"""
        self.context_history = []