import subprocess
import json
from typing import Optional, Dict, List

class GenerationHandler:
    def __init__(self, model_name: str = "mistral"):
        """
        Initialize the generation handler with specified model
        Available models: mistral, llama2, codellama, phi, neural-chat
        """
        self.model = model_name
        self.context_history = []
        self.max_context_length = 5
        self.temperature = 0.7
        self.max_tokens = 500

    def generate_response(self, query: str, context: Optional[Dict] = None) -> str:
        """Generate a response for the given query"""
        try:
            # Add context to history
            if context:
                self.context_history.append({"query": query, "context": context})
                # Keep only recent context
                if len(self.context_history) > self.max_context_length:
                    self.context_history.pop(0)

            # Format the prompt with context
            prompt = self._format_prompt(query)

            # Call Ollama with parameters
            cmd = [
                "ollama", "run",
                self.model,
                "--temperature", str(self.temperature),
                "--max-tokens", str(self.max_tokens),
                prompt
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return self._format_response(result.stdout.strip())
            else:
                return f"Error generating response: {result.stderr}"

        except Exception as e:
            return f"Failed to generate response: {str(e)}"

    def _format_prompt(self, query: str) -> str:
        """Format the prompt with context history and system instructions"""
        system_prompt = f"""You are a helpful AI assistant using the {self.model} model.
        Please provide clear, accurate, and helpful responses.
        If you're unsure about something, please say so.
        For code-related questions, include examples and explanations."""

        formatted_prompt = f"System: {system_prompt}\n\nPrevious context:\n"
        
        for item in self.context_history:
            formatted_prompt += f"Q: {item['query']}\n"
            if item['context']:
                formatted_prompt += f"Context: {json.dumps(item['context'])}\n"
        
        formatted_prompt += f"\nCurrent query: {query}\n"
        return formatted_prompt

    def _format_response(self, response: str) -> str:
        """Format the response for better readability"""
        # Remove any system prompts or artifacts
        lines = response.split('\n')
        cleaned_lines = [line for line in lines if not line.startswith(('System:', 'Assistant:', '>'))]
        
        # Join and clean up the response
        cleaned_response = ' '.join(cleaned_lines).strip()
        return cleaned_response

    def handle_specific_queries(self, query_type: str, query: str) -> str:
        """Handle specific types of generation requests"""
        
        handlers = {
            'code_generation': self._handle_code_generation,
            'explanation': self._handle_explanation,
            'creative_writing': self._handle_creative_writing,
            'general': self._handle_general_query
        }
        
        handler = handlers.get(query_type, self._handle_general_query)
        return handler(query)

    def _handle_code_generation(self, query: str) -> str:
        """Handle code generation requests using CodeLlama model"""
        original_model = self.model
        self.model = "codellama"  # Switch to CodeLlama for code generation
        
        prompt = f"""
        Generate code for the following request:
        {query}
        
        Please provide:
        1. Code implementation
        2. Brief explanation
        3. Example usage
        
        Use appropriate formatting and comments.
        """
        
        response = self.generate_response(prompt)
        self.model = original_model  # Restore original model
        return response

    def _handle_explanation(self, query: str) -> str:
        """Handle explanation requests"""
        prompt = f"""
        Explain the following:
        {query}
        
        Please provide:
        1. Simple explanation
        2. Key concepts
        3. Examples if applicable
        4. Additional resources if relevant
        """
        return self.generate_response(prompt)

    def _handle_creative_writing(self, query: str) -> str:
        """Handle creative writing requests"""
        prompt = f"""
        Create a creative response for:
        {query}
        
        Be imaginative and engaging while maintaining:
        1. Clear narrative structure
        2. Engaging language
        3. Appropriate tone
        """
        return self.generate_response(prompt)

    def _handle_general_query(self, query: str) -> str:
        """Handle general queries"""
        prompt = f"""
        Please respond to this query:
        {query}
        
        Provide a clear, helpful, and accurate response.
        Include relevant examples or explanations if needed.
        """
        return self.generate_response(prompt)

    def clear_context(self):
        """Clear the context history"""
        self.context_history = []

    def set_model_parameters(self, temperature: float = 0.7, max_tokens: int = 500):
        """Update model generation parameters"""
        self.temperature = max(0.0, min(1.0, temperature))  # Clamp between 0 and 1
        self.max_tokens = max(1, max_tokens)  # Ensure positive value