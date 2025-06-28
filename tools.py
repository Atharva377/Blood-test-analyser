import os
from dotenv import load_dotenv
from typing import Any
from crewai.tools import tool  # Fixed: import 'tool' decorator from crewai.tools
load_dotenv()

from crewai_tools import SerperDevTool
from pypdf import PdfReader

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("Blood Test Report Reader")  # Fixed: use @tool decorator with name
def blood_test_report_tool(path: str = 'data/sample.pdf') -> str:
    """Tool to read data from a pdf file containing blood test reports

    Args:
        path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full Blood Test report file
    """
    full_report = ""
    
    # Using PdfReader instead of PDFLoader
    reader = PdfReader(path)
    
    for page in reader.pages:
        content = page.extract_text()
        
        # Clean and format the report data
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
            
        full_report += content + "\n"
        
    return full_report

## Creating Nutrition Analysis Tool
@tool("Nutrition Analysis Tool")  # Fixed: use @tool decorator with name
def nutrition_analysis_tool(blood_report_data: str) -> str:
    """Tool to analyze nutrition based on blood report data"""
    # Process and analyze the blood report data
    processed_data = blood_report_data
    
    # Clean up the data format
    i = 0
    while i < len(processed_data):
        if processed_data[i:i+2] == "  ":  # Remove double spaces
            processed_data = processed_data[:i] + processed_data[i+1:]
        else:
            i += 1
            
    # TODO: Implement nutrition analysis logic here
    return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
@tool("Exercise Planning Tool")  # Fixed: use @tool decorator with name
def exercise_planning_tool(blood_report_data: str) -> str:
    """Tool to create exercise plans based on blood report data"""
    # TODO: Implement exercise planning logic here
    return "Exercise planning functionality to be implemented"