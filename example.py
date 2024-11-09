from nlp_processor import NLPProcessor
from system_commands import SystemCommandExecutor
from generation_handler import GenerationHandler

def main():
    # Initialize the NLP processor, system command executor, and generation handler
    nlp = NLPProcessor()
    cmd_executor = SystemCommandExecutor()
    generator = GenerationHandler()
    
    print("\nEnhanced NLP Command System")
    print("Type 'exit' to quit")
    print("Type 'correct: [correction]' to provide correction")
    print("Type 'good' or 'bad' after each response to provide feedback")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit command
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        if not user_input:
            continue
        
        # Handle corrections
        if user_input.startswith("correct:"):
            correction = user_input[8:].strip()
            nlp.provide_feedback(last_input, False, correction=correction)
            print("Thanks for the correction!")
            continue
            
        # Process the input
        classification = nlp.classify_input(user_input)
        last_input = user_input
        
        print("\nAnalysis Results:")
        print("-" * 30)
        
        if classification['type'] == 'system':
            print(f"✓ System Command Detected (Confidence: {classification['confidence']:.2f})")
            print(f"  Category: {classification['category']}")
            print(f"  Command: {classification['command']}")
            
            # Execute the system command and show the result
            result = cmd_executor.execute_command(
                classification['category'], 
                classification['command']
            )
            print(f"\nExecuting Command:")
            print(f"  → {result}")
            
            print("\nContext Details:")
            print(f"  Word Similarity: {classification['context']['word_similarity']:.2f}")
            print(f"  Sequence Similarity: {classification['context']['sequence_similarity']:.2f}")
            print(f"  Context Score: {classification['context']['context_score']:.2f}")
            if classification['context']['relevant_entities']:
                print("  Relevant Entities:", classification['context']['relevant_entities'])
                
        elif classification['type'] == 'generation':
            print(f"✓ Generation Request Detected (Confidence: {classification['confidence']:.2f})")
            print(f"  Intent: {classification['intent']}")
            
            # Generate response using the generation handler
            print("\nGenerating Response...")
            response = generator.handle_specific_queries(
                classification['intent'],
                user_input
            )
            print(f"\nResponse:")
            print("-" * 30)
            print(response)
            print("-" * 30)
            
            print("\nContext Details:")
            print(f"  Generation Type: {classification['context']['generation_type']}")
            if classification['context']['key_phrases']:
                print("  Key Phrases:", classification['context']['key_phrases'])
                
        else:
            print("? Unclear Command Detected")
            print("\nSuggestions:")
            for suggestion in classification['suggestions']:
                print(f"  - {suggestion['category']}: {suggestion['command']}")
                print(f"    Confidence: {suggestion['confidence']:.2f}")
                if suggestion['context']['relevant_entities']:
                    print(f"    Relevant Entities: {suggestion['context']['relevant_entities']}")
            
            print("\nContext Analysis:")
            print("  Possible Intents:", classification['context']['possible_intents'])
            print("  Key Phrases:", classification['context']['key_phrases'])
            
        print("-" * 50)
        
        # Get feedback
        feedback = input("\nWas this response helpful? (good/bad): ").strip().lower()
        if feedback in ['good', 'bad']:
            nlp.provide_feedback(user_input, feedback == 'good')

if __name__ == "__main__":
    main() 