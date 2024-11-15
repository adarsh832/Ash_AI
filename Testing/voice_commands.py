import speech_recognition as sr
from Processing.nlp_processor import NLPProcessor
from Processing.system_commands import SystemCommandExecutor
from Processing.generation_handler import GenerationHandler
import pyttsx3
import threading

class VoiceCommander:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.nlp = NLPProcessor()
        self.cmd_executor = SystemCommandExecutor()
        self.generator = GenerationHandler()
        self.engine = pyttsx3.init()
        self.is_listening = False
        
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands"""
        with sr.Microphone() as source:
            print("\nListening... (say 'stop listening' to exit)")
            self.speak("Listening... say your command")
            self.is_listening = True
            
            while self.is_listening:
                try:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source)
                    # Listen for input
                    audio = self.recognizer.listen(source)
                    
                    # Convert speech to text
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"\nYou said: {command}")
                    
                    # Check for stop command
                    if command in ['stop listening', 'exit', 'quit', 'bye']:
                        self.speak("Stopping voice commands")
                        self.is_listening = False
                        break
                    
                    # Process the command
                    classification = self.nlp.classify_input(command)
                    
                    if classification['type'] == 'system':
                        print(f"Executing: {classification['command']}")
                        self.speak(f"Executing {classification['command']}")
                        
                        result = self.cmd_executor.execute_command(
                            classification['category'],
                            classification['command']
                        )
                        print(f"Result: {result}")
                        self.speak(result)
                        
                    elif classification['type'] == 'generation':
                        print(f"Processing question: {command}")
                        self.speak("Let me think about that")
                        
                        response = self.generator.handle_specific_queries(
                            classification['intent'],
                            command
                        )
                        
                        print(f"Response: {response}")
                        self.speak(response)
                        
                    else:
                        suggestions = [f"{s['category']}: {s['command']}" 
                                     for s in classification['suggestions']]
                        response = "I'm not sure what you want. Did you mean: " + \
                                 " or ".join(suggestions)
                        print(response)
                        self.speak(response)
                    
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    self.speak("Sorry, I didn't catch that")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    self.speak("Sorry, there was an error processing your request")
                except Exception as e:
                    print(f"Error: {e}")
                    self.speak("An error occurred")

def main():
    print("Voice Command System")
    print("-------------------")
    commander = VoiceCommander()
    commander.listen()

if __name__ == "__main__":
    main() 