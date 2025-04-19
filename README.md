# Subtitle Translator
A Python application for translating subtitle files between different languages.
## Overview
This project provides a tool for automatically translating subtitle files (.srt, .ass, etc.) while maintaining their original timing and formatting. It's designed to help you quickly create translated subtitles for videos in different languages.
## Features
- Support for common subtitle formats
- High-quality translations using language service APIs
- Preservation of original subtitle timing and formatting
- Command-line interface for easy integration with scripts and workflows

## Installation
1. Clone the repository:
``` bash
   git clone https://github.com/yourusername/subtitle-translator.git
   cd subtitle-translator
```
1. Create and activate a virtual environment:
``` bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
1. Install the required dependencies:
``` bash
   pip install -r src/requirements.txt
```
1. Set up environment variables by creating a file with your API keys (see Configuration section) `.env`

## Usage
Run the application with the following command:
``` bash
python src/main.py --input path/to/subtitles.srt --output path/to/output.srt --source-lang en --target-lang fr
```
### Command-line Arguments
- `--input`: Path to the input subtitle file
- `--output`: Path where the translated subtitle file will be saved
- `--source-lang`: Source language code (e.g., 'en' for English)
- `--target-lang`: Target language code (e.g., 'fr' for French)
- `--service`: Translation service to use (default: depends on configuration)

## Configuration
Create a file in the project root with your API keys: `.env`
``` 
# Translation API keys
LMSTUDIO_API_URL=your_api_url
MODEL_ID=your_loaded_model_id
```
## Project Structure
``` 
subtitle-translator/
├── .env                    # Environment variables
├── README.md               # This documentation
└── src/                    # Source code
    ├── main.py             # Main entry point
    ├── requirements.txt    # Python dependencies
    └── subtitle_translator/
        ├── core/           # Core functionality
        ├── services/       # Translation service adapters
        └── utils/          # Utility functions
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
