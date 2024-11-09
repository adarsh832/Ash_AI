import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from functools import lru_cache
from ollama_generator import OllamaGenerator
import json
from spellchecker import SpellChecker
import os
from datetime import datetime
from collections import defaultdict

class NLPProcessor:
    def __init__(self, language='en', model_name="llama2"):
        # Download required NLTK resources
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        # Initialize spaCy model
        self.nlp = spacy.load('en_core_web_sm')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize Ollama generator
        self.generator = OllamaGenerator(model_name)
        
        # Define system command patterns
        self.system_commands = {
            'volume': [
                'increase volume', 'decrease volume', 'mute', 'unmute',
                'volume up', 'volume down', 'set volume', 'max volume',
                'min volume', 'adjust volume'
            ],
            'brightness': [
                'increase brightness', 'decrease brightness', 'max brightness',
                'min brightness', 'adjust brightness', 'set brightness',
                'screen brighter', 'screen dimmer'
            ],
            'power': [
                'shutdown', 'restart', 'sleep', 'wake up', 'hibernate',
                'power off', 'turn off', 'reboot', 'log out', 'sign out',
                'lock screen', 'unlock screen'
            ],
            'app': [
                'open', 'close', 'start', 'stop', 'launch', 'quit',
                'minimize', 'maximize', 'restore', 'force quit',
                'switch to', 'focus on', 'run app', 'kill app'
            ],
            'system': [
                'update', 'install', 'uninstall', 'check status',
                'clean temp', 'clear cache', 'check memory', 'check cpu',
                'check storage', 'system info', 'task manager'
            ],
            'network': [
                'wifi on', 'wifi off', 'connect wifi', 'disconnect wifi',
                'bluetooth on', 'bluetooth off', 'airplane mode',
                'check internet', 'network status', 'show wifi networks'
            ],
            'media': [
                'play', 'pause', 'stop', 'next', 'previous', 'fast forward',
                'rewind', 'shuffle', 'repeat', 'mute audio', 'unmute audio'
            ],
            'file': [
                'copy', 'paste', 'cut', 'delete', 'rename', 'move',
                'new folder', 'new file', 'compress', 'extract',
                'download', 'upload', 'share', 'search files'
            ],
            'display': [
                'change resolution', 'rotate screen', 'mirror display',
                'extend display', 'night mode', 'dark mode', 'light mode',
                'change wallpaper', 'screen saver'
            ],
            'input': [
                'enable keyboard', 'disable keyboard', 'enable touchpad',
                'disable touchpad', 'enable mouse', 'disable mouse',
                'keyboard layout', 'input language'
            ],
            'security': [
                'enable firewall', 'disable firewall', 'scan virus',
                'update antivirus', 'check permissions', 'encrypt',
                'decrypt', 'backup data', 'restore backup'
            ],
            'accessibility': [
                'enable narrator', 'disable narrator', 'high contrast',
                'magnifier on', 'magnifier off', 'voice control',
                'closed captions', 'screen reader'
            ]
        }
        
        # Initialize spell checker
        self.spell = SpellChecker()
        
        # Add learning-related initialization
        self.learning_file = "nlp_learning.json"
        self.interaction_history = self._load_learning_data()
        self.command_patterns = defaultdict(float)
        self.confidence_threshold = 0.6  # Adjustable threshold
        
    @lru_cache(maxsize=1000)
    def preprocess_text(self, text):
        """Clean and preprocess the input text with caching"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) 
                 for token in tokens 
                 if token not in self.stop_words]
        
        return tokens
    
    @lru_cache(maxsize=1000)
    def extract_entities(self, text):
        """Extract named entities using spaCy with caching"""
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
    def get_pos_tags(self, text):
        """Get Part of Speech tags"""
        doc = self.nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        return pos_tags
    
    def get_dependencies(self, text):
        """Get dependency parsing"""
        doc = self.nlp(text)
        dependencies = [(token.text, token.dep_, token.head.text) 
                       for token in doc]
        return dependencies
    
    def batch_process(self, texts, batch_size=32):
        """Process multiple texts efficiently"""
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            docs = list(self.nlp.pipe(batch))
            batch_results = [
                {
                    'entities': [(ent.text, ent.label_) for ent in doc.ents],
                    'pos_tags': [(token.text, token.pos_) for token in doc],
                    'dependencies': [(token.text, token.dep_, token.head.text) 
                                   for token in doc]
                }
                for doc in docs
            ]
            results.extend(batch_results)
        return results
    
    def analyze_and_generate(self, input_text):
        """Analyze text and generate appropriate response"""
        # Preprocess and analyze the input
        tokens = self.preprocess_text(input_text)
        entities = self.extract_entities(input_text)
        pos_tags = self.get_pos_tags(input_text)
        
        # Create context from analysis
        context = {
            "entities": entities,
            "pos_tags": pos_tags,
            "preprocessed_tokens": tokens
        }
        
        return {
            "analysis": context,
            "generated_response": self.generator.generate_with_context(
                input_text, 
                json.dumps(context)
            )
        }
    
    def process_conversation(self, user_input, conversation_history=None):
        """Process conversation with context"""
        # Analyze current input
        analysis = self.analyze_and_generate(user_input)
        
        # Include conversation history if available
        if conversation_history:
            context = f"Previous conversation: {conversation_history}\n"
            context += f"Current analysis: {json.dumps(analysis['analysis'])}"
        else:
            context = f"Analysis: {json.dumps(analysis['analysis'])}"
            
        response = self.generator.generate_with_context(user_input, context)
        return response
    
    def _correct_spelling(self, text):
        """Correct spelling mistakes in the input text with improved handling"""
        # Words to preserve (don't correct these)
        preserve_words = {
            # Programming terms
            'python', 'java', 'javascript', 'cpp', 'html', 'css', 'sql',
            'api', 'json', 'xml', 'npm', 'git', 'docker', 'kubernetes',
            # Common abbreviations
            'ai', 'ml', 'nlp', 'api', 'gui', 'cli', 'sdk', 'ide',
            # Technical terms
            'regex', 'async', 'sync', 'crud', 'dom', 'url', 'uri',
            # File extensions
            'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv',
            # Common names and brands
            'google', 'microsoft', 'apple', 'linux', 'windows', 'mac',
            'chrome', 'firefox', 'safari', 'edge', 'vscode'
        }

        words = text.split()
        corrected_words = []
        corrections_made = False
        
        for word in words:
            word_lower = word.lower()
            
            # Skip correction if word should be preserved
            if word_lower in preserve_words:
                corrected_words.append(word)
                continue
                
            # Check if the word is misspelled
            if word_lower in self.spell:  # Word exists in dictionary
                corrected_words.append(word)
            else:
                # Get the correction
                correction = self.spell.correction(word)
                if correction and correction != word:
                    corrected_words.append(correction)
                    corrections_made = True
                else:
                    corrected_words.append(word)
        
        corrected_text = ' '.join(corrected_words)
        
        return {
            'corrected_text': corrected_text,
            'original_text': text,
            'corrections_made': corrections_made
        }
    
    def classify_input(self, text):
        """Enhanced classification with improved app command handling"""
        # Process the text
        tokens = self.preprocess_text(text)
        entities = self.extract_entities(text)
        pos_tags = self.get_pos_tags(text)
        doc = self.nlp(text)
        
        # Check for app commands first
        text_parts = text.lower().split()
        if len(text_parts) >= 2 and text_parts[0] in self.system_commands['app']:
            return {
                'type': 'system',
                'category': 'app',
                'command': text,  # Use full text as command
                'confidence': 0.9,
                'context': {
                    'word_similarity': 0.9,
                    'sequence_similarity': 0.9,
                    'context_score': 0.9,
                    'relevant_entities': [e for e, _ in entities]
                }
            }
        
        # Check for system commands first
        highest_confidence = 0
        matched_command = None
        matched_category = None
        
        for category, commands in self.system_commands.items():
            for cmd in commands:
                confidence = self._sequence_match(cmd, text)
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    matched_command = cmd
                    matched_category = category
        
        # Apply learned confidence adjustments
        pattern = text.lower()
        if pattern in self.interaction_history["confidence_adjustments"]:
            learned_confidence = self.interaction_history["confidence_adjustments"][pattern]
            highest_confidence = (highest_confidence + learned_confidence) / 2
        
        # If high confidence in system command
        if highest_confidence > 0.6:
            context_score = self._calculate_context_score(
                matched_category, 
                text, 
                entities, 
                pos_tags
            )
            return {
                'type': 'system',
                'category': matched_category,
                'command': matched_command,
                'confidence': highest_confidence,
                'context': {
                    'word_similarity': highest_confidence,
                    'sequence_similarity': self._sequence_match(matched_command, text),
                    'context_score': context_score,
                    'relevant_entities': [e for e, _ in entities]
                }
            }
        
        # Check for generation request
        generation_score = self._calculate_generation_score(text, tokens, doc)
        if generation_score > 0.3:  # Lower threshold for better question detection
            return {
                'type': 'generation',
                'confidence': generation_score,
                'intent': self._determine_generation_intent(doc),
                'context': {
                    'generation_type': 'text',
                    'key_phrases': [token for token in tokens if len(token) > 3]
                }
            }
        
        # If no clear classification, return suggestions
        suggestions = self._get_enhanced_suggestions(text, tokens, entities, pos_tags)
        return {
            'type': 'unclear',
            'suggestions': suggestions,
            'context': {
                'possible_intents': [s['category'] for s in suggestions],
                'key_phrases': [token for token in tokens if len(token) > 3]
            }
        }
    
    def provide_feedback(self, input_text, was_successful, correction=None):
        """Allow users to provide feedback on classifications"""
        self.record_interaction(
            input_text=input_text,
            classification=self.classify_input(input_text),
            success=was_successful,
            correction=correction
        )
    
    def _sequence_match(self, cmd, text):
        """Calculate sequence matching score with improved app command handling"""
        import difflib
        
        # Convert to lowercase for comparison
        text_lower = text.lower()
        cmd_lower = cmd.lower()
        
        # Special handling for app commands
        text_parts = text_lower.split()
        cmd_parts = cmd_lower.split()
        
        if len(text_parts) >= 2 and text_parts[0] in self.system_commands['app']:
            # If this is an app command (e.g., "open whatsapp")
            if text_parts[0] == cmd_parts[0]:  # If the action matches (e.g., "open")
                return 0.9  # High confidence for app commands
            return 0.0  # No match if actions don't match
        
        # Regular sequence matching for other commands
        matcher = difflib.SequenceMatcher(None, cmd_lower, text_lower)
        return matcher.ratio()
    
    def _calculate_context_score(self, category, text, entities, pos_tags):
        """Calculate context relevance score"""
        score = 0.0
        
        # Category-specific keywords
        category_keywords = {
            'volume': ['sound', 'audio', 'speaker', 'loud', 'quiet'],
            'brightness': ['screen', 'display', 'dim', 'light', 'dark'],
            'power': ['system', 'computer', 'device', 'machine'],
            # Add more categories...
        }
        
        # Check for category-specific keywords
        if category in category_keywords:
            keywords = set(category_keywords[category])
            text_words = set(text.lower().split())
            keyword_matches = keywords.intersection(text_words)
            score += len(keyword_matches) * 0.2
        
        # Check for relevant entities
        for entity, label in entities:
            if self._is_relevant_entity(entity, category):
                score += 0.15
        
        # Check for relevant POS patterns
        score += self._check_pos_patterns(pos_tags, category) * 0.15
        
        return min(score, 1.0)  # Normalize to max 1.0
    
    def _calculate_generation_score(self, text, tokens, doc):
        """Calculate generation request confidence with improved detection"""
        score = 0.0
        
        # Expanded generation indicators
        generation_indicators = {
            'high': [
                'tell', 'explain', 'write', 'generate', 'create', 'make', 'show',
                'describe', 'elaborate', 'define', 'what', 'how', 'why', 'when',
                'who', 'where', 'which'
            ],
            'medium': [
                'is', 'are', 'was', 'were', 'will', 'can', 'could', 'would',
                'should', 'may', 'might', 'do', 'does', 'did', 'mean', 'work',
                'function', 'help', 'guide', 'teach'
            ],
            'low': [
                'the', 'a', 'an', 'any', 'some', 'many', 'few', 'about',
                'like', 'similar', 'different', 'other'
            ]
        }
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Check for question marks (highest priority)
        if '?' in text:
            score += 0.5
        
        # Check for question words at the start
        first_word = text_lower.split()[0] if text_lower else ''
        if first_word in generation_indicators['high']:
            score += 0.4
        
        # Check tokens against indicators
        for token in tokens:
            token_lower = token.lower()
            if token_lower in generation_indicators['high']:
                score += 0.3
            elif token_lower in generation_indicators['medium']:
                score += 0.2
            elif token_lower in generation_indicators['low']:
                score += 0.1
        
        # Check for question structure
        if self._is_question_structure(doc):
            score += 0.3
        
        # Check for imperative mood (commands/requests)
        if len(doc) > 0 and doc[0].pos_ == 'VERB':
            score += 0.2
        
        # If not a system command and contains words, give minimum score
        if score == 0 and len(tokens) > 0:
            score = 0.3  # Base score for any non-empty input
        
        # Normalize score
        score = min(score, 1.0)
        
        # If it's clearly not a system command and has some words, boost the score
        if score > 0.2 and not any(
            cmd in text_lower 
            for cmds in self.system_commands.values() 
            for cmd in cmds
        ):
            score += 0.2
            score = min(score, 1.0)
        
        return score
    
    def _get_enhanced_suggestions(self, text, tokens, entities, pos_tags):
        """Get improved command suggestions"""
        suggestions = []
        
        # Get base suggestions
        base_suggestions = self._get_suggestions(text)
        
        # Enhance with context
        for suggestion in base_suggestions:
            confidence = self._calculate_context_score(
                suggestion['category'],
                text,
                entities,
                pos_tags
            )
            suggestion['confidence'] = confidence
            suggestion['context'] = {
                'relevant_entities': [
                    e for e in entities 
                    if self._is_relevant_entity(e[0], suggestion['category'])
                ],
                'pos_pattern': self._check_pos_patterns(
                    pos_tags, 
                    suggestion['category']
                )
            }
            suggestions.append(suggestion)
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        return suggestions[:3]
    
    def _get_suggestions(self, text):
        """Get possible command suggestions for unclear input"""
        suggestions = []
        tokens = set(text.lower().split())
        
        # Look for partial matches
        for category, commands in self.system_commands.items():
            for command in commands:
                command_tokens = set(command.split())
                if any(token in tokens for token in command_tokens):
                    suggestions.append({
                        'category': category,
                        'command': command
                    })
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _determine_generation_intent(self, doc):
        """Determine the specific generation intent"""
        # Check for coding-related requests
        code_indicators = ['code', 'program', 'script', 'function']
        for token in doc:
            if token.text.lower() in code_indicators:
                return 'code_generation'
        
        # Check for creative writing requests
        creative_indicators = ['story', 'joke', 'poem']
        for token in doc:
            if token.text.lower() in creative_indicators:
                return 'creative_writing'
        
        # Check for explanatory requests
        if any(token.text.lower() in ['explain', 'how', 'why'] for token in doc):
            return 'explanation'
            
        return 'general'
    
    def _is_question_structure(self, doc):
        """Check if the text has a question-like structure"""
        # Initialize as False
        has_question_structure = False
        
        # Question-related POS patterns
        question_starts = ['WDT', 'WP', 'WP$', 'WRB']  # What, Who, Whose, When, etc.
        aux_verbs = ['MD', 'VBZ', 'VBP', 'VBD']  # Modal verbs, Is, Are, Was, etc.
        
        # Check if sentence starts with question word or auxiliary verb
        if len(doc) > 0:
            first_token = doc[0]
            if first_token.tag_ in question_starts:
                has_question_structure = True
            elif first_token.tag_ in aux_verbs:
                has_question_structure = True
                
            # Check for inverted subject-verb structure
            if len(doc) > 2:
                if (first_token.tag_ in aux_verbs and 
                    doc[1].pos_ in ['PRON', 'PROPN', 'NOUN']):
                    has_question_structure = True
        
        return has_question_structure
    
    def _check_pos_patterns(self, pos_tags, category):
        """Check for relevant POS patterns based on category"""
        score = 0.0
        
        # Category-specific POS patterns
        patterns = {
            'volume': ['VERB', 'NOUN'],  # e.g., "increase volume"
            'brightness': ['VERB', 'NOUN'],  # e.g., "adjust brightness"
            'power': ['VERB'],  # e.g., "shutdown"
            'app': ['VERB', 'PROPN'],  # e.g., "open Chrome"
            # Add more patterns as needed
        }
        
        if category in patterns:
            expected_pattern = patterns[category]
            pos_sequence = [tag for _, tag in pos_tags]
            
            # Check if the expected pattern appears in the sequence
            for i in range(len(pos_sequence) - len(expected_pattern) + 1):
                if pos_sequence[i:i+len(expected_pattern)] == expected_pattern:
                    score += 1.0
                    break
        
        return min(score, 1.0)
    
    def _is_relevant_entity(self, entity, category):
        """Check if entity is relevant for the given category"""
        # Category-specific relevant entity types
        relevant_entities = {
            'app': ['PRODUCT', 'ORG', 'GPE'],  # Software names, organizations
            'file': ['FILE', 'PATH'],  # File names and paths
            'network': ['ORG', 'GPE'],  # Network names, locations
            'security': ['ORG', 'PERSON'],  # Security-related entities
            # Add more categories as needed
        }
        
        if category in relevant_entities:
            return any(entity.lower() in self.system_commands[category])
        
        return False
    
    def _load_learning_data(self):
        """Load previous learning data if it exists"""
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except:
                return {
                    "command_patterns": {},
                    "user_corrections": [],
                    "successful_commands": [],
                    "confidence_adjustments": {}
                }
        return {
            "command_patterns": {},
            "user_corrections": [],
            "successful_commands": [],
            "confidence_adjustments": {}
        }
    
    def _save_learning_data(self):
        """Save learning data to file"""
        with open(self.learning_file, 'w') as f:
            json.dump(self.interaction_history, f, indent=2)
    
    def record_interaction(self, input_text, classification, success=None, correction=None):
        """Record interaction for learning"""
        timestamp = datetime.now().isoformat()
        interaction = {
            "timestamp": timestamp,
            "input": input_text,
            "classification": classification,
            "success": success,
            "correction": correction
        }
        
        # Update pattern confidence based on success/failure
        if success is not None:
            pattern = input_text.lower()
            current_confidence = self.interaction_history["confidence_adjustments"].get(pattern, 0.5)
            
            if success:
                # Increase confidence for successful patterns
                new_confidence = min(1.0, current_confidence + 0.1)
                self.interaction_history["successful_commands"].append(interaction)
            else:
                # Decrease confidence for failed patterns
                new_confidence = max(0.0, current_confidence - 0.05)
            
            self.interaction_history["confidence_adjustments"][pattern] = new_confidence
        
        # Record corrections for learning
        if correction:
            self.interaction_history["user_corrections"].append({
                "original": input_text,
                "correction": correction,
                "timestamp": timestamp
            })
        
        self._save_learning_data()