from flask import Flask, render_template, request, jsonify
from nlp_processor import NLPProcessor
from system_commands import SystemCommandExecutor
from generation_handler import GenerationHandler

app = Flask(__name__)

# Initialize our components
nlp = NLPProcessor()
cmd_executor = SystemCommandExecutor()
generator = GenerationHandler()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_command():
    user_input = request.json.get('command', '')
    
    # Process the input
    classification = nlp.classify_input(user_input)
    
    response = {
        'type': classification['type'],
        'confidence': classification['confidence'],
        'result': ''
    }
    
    if classification['type'] == 'system':
        result = cmd_executor.execute_command(
            classification['category'],
            classification['command']
        )
        response['result'] = result
        response['category'] = classification['category']
        
    elif classification['type'] == 'generation':
        response['result'] = generator.handle_specific_queries(
            classification['intent'],
            user_input
        )
        
    else:
        response['result'] = "Unclear command. Please try again."
        response['suggestions'] = classification['suggestions']
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True) 