import os
from dotenv import load_dotenv
from typing import Any
from crewai.tools import tool
load_dotenv()

from crewai_tools import SerperDevTool
from pypdf import PdfReader

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

## Creating search tool
search_tool = SerperDevTool()

## Improved PDF reader tool
@tool("Blood Test Report Reader")
def blood_test_report_tool(path: str) -> str:
    """Read and extract text from blood test PDF reports"""
    try:
        if not path or not os.path.exists(path):
            return "ERROR: File not found or invalid path"
        
        reader = PdfReader(path)
        if len(reader.pages) == 0:
            return "ERROR: PDF file is empty or corrupted"
        
        # Extract text with better handling
        extracted_text = ""
        for i, page in enumerate(reader.pages[:3]):  # Limit to first 3 pages
            page_text = page.extract_text()
            if page_text:
                extracted_text += f"\n--- Page {i+1} ---\n{page_text}"
            
            if len(extracted_text) > 3000:  # Limit total text
                break
        
        if not extracted_text.strip():
            return "ERROR: No readable text found in PDF"
            
        return extracted_text[:3000]  # Return first 3000 characters
        
    except Exception as e:
        return f"ERROR reading PDF: {str(e)[:100]}"