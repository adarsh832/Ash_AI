# Ash - AI Voice Command System
# Run this app with Gui Interface to use it as a voice assistant (app.py)

An advanced AI-powered voice command system that can control your computer through natural language commands and respond to questions using LLM (Language Learning Models).

## Most important to download is Ollama and install llama3.2 model or it will not generate response

## Features

- 🎙️ Voice Command Recognition
- 🤖 Natural Language Processing
- 💻 System Control Commands
- 🔊 Voice Feedback
- 📚 Question Answering
- 🧠 Learning Capabilities
- 🔄 Context Awareness

## Interface Features

1. **Command Line Interface**
   - Text-based input and output
   - Command history
   - Auto-completion support
   - Color-coded responses

2. **Voice Interface**
   - Wake word detection ("Hey Ash")
   - Real-time voice recognition
   - Natural speech responses
   - Background noise filtering
   - Multi-language support

3. **GUI Interface**
   - Clean, modern design
   - Command visualization
   - System status indicators
   - Settings configuration panel
   - Command history viewer

## System Commands Available

1. **App Control**
   - Open applications (`open chrome`, `open notepad`)
   - Close applications (`close chrome`)
   - Minimize/Maximize windows (`minimize all`, `minimize current`)

2. **Volume Control**
   - Adjust volume (`increase volume`, `decrease volume`)
   - Mute/Unmute (`mute`, `unmute`)
   - Set volume levels (`max volume`, `min volume`)

3. **Brightness Control**
   - Adjust brightness (`increase brightness`, `decrease brightness`)
   - Set brightness levels (`max brightness`, `min brightness`)

4. **Power Management**
   - System power (`shutdown`, `restart`)
   - Power states (`sleep`, `hibernate`)
   - Session control (`lock screen`, `log out`)

5. **Network Management**
   - WiFi control (`wifi on`, `wifi off`)
   - Network info (`check internet`, `show wifi networks`)
   - Bluetooth (`bluetooth on`, `bluetooth off`)

6. **Display Settings**
   - Display modes (`night mode`, `dark mode`, `light mode`)
   - Screen control (`rotate screen`, `change resolution`)
   - Multi-display (`mirror display`, `extend display`)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/adarsh832/AI.git
   cd ai-voice-command
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Additional Requirements**
   - Windows: Download [NirCmd](https://www.nirsoft.net/utils/nircmd.html) for volume control
   - Linux: Install required packages
     ```bash
     sudo apt-get install wmctrl xdotool
     ```
   - macOS: Install additional tools
     ```bash
     brew install brightness
     ```

## Usage

1. **Run with Text Input**
   ```bash
   python example.py
   ```

2. **Run with Voice Commands**
   ```bash
   python voice_commands.py
   ```
3. **Run with GUI**
   ```bash
   python app.py
   ```

3. **Voice Command Examples**
   - "Open Chrome"
   - "Increase volume"
   - "What is Python?"
   - "Minimize all windows"
   - "Check internet connection"

## Project Structure

```
ai-voice-command/
├── commands/                    # Command implementation modules
│   ├── __init__.py            # Package initializer
│   ├── accessibility_commands.py # Accessibility features control
│   ├── app_commands.py        # Application control
│   ├── brightness_commands.py  # Screen brightness control
│   ├── display_commands.py    # Display settings control
│   ├── file_commands.py       # File operations
│   ├── input_commands.py      # Input device control
│   ├── media_commands.py      # Media playback control
│   ├── network_commands.py    # Network and connectivity
│   ├── power_commands.py      # Power management
│   ├── security_commands.py   # Security features
│   ├── system_commands.py     # System operations
│   └── volume_commands.py     # Audio volume control
│
├── example.py                  # Text-based interface
├── voice_commands.py          # Voice command interface
├── nlp_processor.py           # Natural Language Processing
├── generation_handler.py      # LLM response generation
├── ollama_generator.py        # Ollama integration
├── system_commands.py         # Command executor
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

### Key Components

1. **Command Modules** (`commands/`)
   - Separate modules for different command categories
   - Platform-specific implementations
   - Error handling and feedback

2. **Core Files**
   - `example.py`: Text interface for testing
   - `voice_commands.py`: Voice command interface
   - `nlp_processor.py`: Natural language understanding
   - `generation_handler.py`: AI response generation

3. **Integration**
   - `ollama_generator.py`: LLM integration
   - `system_commands.py`: System command execution

### Command Categories

1. **System Control**
   - App management
   - Volume control
   - Brightness adjustment
   - Power management

2. **Network & Connectivity**
   - WiFi control
   - Bluetooth management
   - Internet connectivity

3. **Display & Interface**
   - Screen settings
   - Display modes
   - Input devices

4. **Security & Files**
   - File operations
   - Security features
   - System protection

5. **Accessibility**
   - Screen readers
   - Visual aids
   - Input assistance

### Development Structure

1. **Core Logic**
   - NLP processing
   - Command classification
   - Voice recognition

2. **Command Execution**
   - Platform detection
   - Command routing
   - Error handling

3. **User Interface**
   - Text interface
   - Voice interface
   - Feedback system

4. **AI Integration**
   - LLM connection
   - Response generation
   - Context management