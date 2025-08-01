import os
from dotenv import load_dotenv
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
import streamlit as st

load_dotenv()

# Load LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Define your PDF path (sample file)
pdf_path = './pdf/Finacle Core 11_13 Data Dictionary.pdf'

# Verify PDF file exists
if not os.path.exists(pdf_path):
    st.error(f"PDF file not found at {pdf_path}. Please ensure the file exists in the correct location.")
    pdf_path = st.file_uploader("Upload Finacle Core Data Dictionary PDF", type=['pdf'])
    if pdf_path is None:
        st.stop()

# Set up PDF Tool
pdf_tools = [PDFSearchTool(pdf=pdf_path)]

# ---------------------- AGENTS ----------------------

# Agent 1: Table Search Agent
table_pdf_search_agent = Agent(
    name='TableSearchAgent',
    role='Finacle PDF Table Locator',
    verbose=False,
    memory=True,
    goal='Locate and retrieve the correct table section from the Finacle Core files based on user input: {topic}',
    backstory=(
        "You are an expert in navigating massive Finacle Core data dictionaries. "
        "You specialize in identifying and extracting the relevant table section based on exact table names. "
        "You work with unstructured and scanned documents and understand the naming conventions used in banking PDFs."
    ),
    tools=pdf_tools,
    rules=[
        'Always look for exact table name matches first.',
        'Return the raw table block containing metadata, comments, and fields details.',
        'Ignore duplicated or outdated definitions.'
    ],
    allow_delegation=True,
    llm=llm
)

# Agent 2: Metadata Extractor
table_parser_agent = Agent(
    name='TableParserAgent',
    role='Finacle Table Metadata Extractor',
    verbose=False,
    memory=True,
    goal='Parse the raw PDF block of table and extract metadata like table name, comments, fields, data types, and more. {topic}',
    backstory=(
        "You are a domain-trained metadata interpreter. "
        "Your job is to carefully read through raw blocks of PDF content and extract all metadata including field names, types, and descriptions."
    ),
    rules=[
        'Extract all field rows, including wrapped or multi-line fields.',
        'Detect if the field block continues onto the next line or page.',
        'Maintain accuracy in the field name and description extraction.'
    ],
    tools=pdf_tools,
    allow_delegation=True,
    llm=llm
)

# Agent 3: Table Formatter
table_formatter_agent = Agent(
    name='TableFormatterAgent',
    role='Senior Table Formatter',
    verbose=False,
    memory=True,
    goal='Convert the extracted metadata into a neatly structured table for user display. {topic}',
    backstory=(
        "You specialize in formatting technical data into user-friendly output. "
        "You work with metadata extracted from banking tables and produce a clean tabular format matching the Finacle Data Dictionary standard."
    ),
    rules=[
        'Always display fields in order as in the document.',
        'Ensure column alignment and readability.'
    ],
    tools=pdf_tools,
    allow_delegation=False,
    llm=llm
)

# Agent 4: Final Responder
table_answer_agent = Agent(
    name='TableAnswerAgent',
    role='Final User-facing Response Agent',
    verbose=False,
    memory=True,
    goal='Deliver the final answer to the user query in a clean and easy-to-read format. {topic}',
    backstory=(
        "You are the final responder. After the search, parse, and format stages, your role is to deliver the result clearly. "
        "You summarize and present the metadata or guide the user on the next steps."
    ),
    rules=[
        'Never modify or interpret table data.',
        'Always thank the user for the prompt.',
        'Maintain a professional tone aligned with banking support systems.'
    ],
    tools=pdf_tools,
    allow_delegation=False,
    llm=llm
)

# ---------------------- TASKS ----------------------

# Task 1: Search Table Task
search_table_task = Task(
    name='Search Table Task',
    description=(
        "Search the Finacle PDFs and locate the complete section: {topic}. "
        "It must correspond to the table name given by the user and include all field details."
    ),
    expected_output='Full raw block containing metadata, field definitions, and extended table lines for {topic}',
    tools=pdf_tools,
    agent=table_pdf_search_agent
)

# Task 2: Extract Metadata
extract_metadata_task = Task(
    name="Extract Metadata Task",
    description=(
        "From the raw table block provided, extract the following structured details:\n"
        "- Table Name\n"
        "- Table Synonym\n"
        "- Table Comments\n"
        "- Module Name\n"
        "- Key Field name\n"
        "- Data type\n"
        "- Description\n"
        "- Foreign keys\n"
        "- Field name\n"
        "- Data type\n"
        "- Description"
    ),
    expected_output="A dictionary or JSON object with all the metadata fields extracted.",
    agent=table_parser_agent
)

# Task 3: Build Structured Table
build_structured_table_task = Task(
    name="Build Structured Table Task",
    description=(
        "Take the extracted metadata and format it into a clean tabular format. "
        "Output should display fields in a structured markdown table matching Finacle Data Dictionary standards."
    ),
    expected_output="A markdown table showing field metadata in an aligned format.",
    agent=table_formatter_agent
)

# Task 4: Respond to User
respond_to_user_task = Task(
    name="Respond to User Task",
    description=(
        "Present the final formatted table back to the user in a clear, helpful tone. "
        "If the table was not found, return a polite message."
    ),
    expected_output="A friendly response including the structured table or an error message.",
    agent=table_answer_agent
)

# ---------------------- CREW WORKFLOW ----------------------

crew = Crew(
    agents=[
        table_pdf_search_agent,
        table_parser_agent,
        table_formatter_agent,
        table_answer_agent
    ],
    tasks=[
        search_table_task,
        extract_metadata_task,
        build_structured_table_task,
        respond_to_user_task
    ],
    process=Process.sequential,
    cache=True,
    max_rpm=100,
    share_crew=True,
)

# ---------------------- EXECUTION ----------------------
st.set_page_config(page_title="Finacle Data Table Search", layout="centered")
st.title("🔍 Finacle Table Metadata Explorer")

# Add text input field
user_input = st.text_input("Enter table name or topic to search:", "")

if st.button("Search") and user_input:
    with st.spinner("Processing with CrewAI agents..."):
        try:
            result = crew.kickoff(inputs={"topic": user_input})
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    st.run()
    
    
  
