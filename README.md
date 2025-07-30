# Finacle Table Metadata Explorer

A streamlit-based application that uses CrewAI and LangChain to search and explore Finacle Core Data Dictionary pdf. The application employs multiple AI agents to search, parse, and present table metadata in a user-friendly format.

## Features

- 🔍 Intelligent PDF searching for table metadata
- 📊 Automated metadata extraction from tables
- 🎯 Precise table formatting and presentation
- 🤖 Multi-agent system using CrewAI
- 🌐 User-friendly Streamlit interface

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Finacle Core Data Dictionary PDF file

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Finacle_AI
```

2. Create a virtual environment:
```bash
pyenv install 3.11.13
pyenv shell 3.11.13
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python --version
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

5. Place your Finacle Core Data Dictionary PDF in the `pdf` directory:
```bash
mkdir pdf
# Copy your "Finacle Core 11_13 Data Dictionary.pdf" to the pdf directory
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter your table name or topic in the search box and click the "Search" button

4. The application will:
   - Search for the table in the PDF
   - Extract relevant metadata
   - Format the information
   - Present it in a clean, readable format

## Project Structure

- `main.py`: Main application file containing the CrewAI agents and Streamlit interface
- `requirements.txt`: List of Python dependencies
- `pdf/`: Directory containing the Finacle Core Data Dictionary PDF
- `.env`: Environment variables file (not tracked in git)

## Agents Description

1. **TableSearchAgent**: Locates and retrieves table sections from pdf
2. **TableParserAgent**: Extracts structured metadata from raw PDF blocks
3. **TableFormatterAgent**: Formats metadata into clean, readable tables
4. **TableAnswerAgent**: Presents final results to users
# Finacle_AI
# Finacle_AI
# Finacle_AI
# Finacle_AI
# Finacle_AI
# Finacle_AI
# Finacle_AI
# Finacle_AI
