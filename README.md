# 🩺 Blood Test Report Analyzer

AI-powered FastAPI application that analyzes blood test PDF reports using CrewAI agents and Groq LLM.

## 🐛 Bugs Fixed

### 1. Dependency Management
- ✅ Resolved dependency conflicts in requirements.txt
- ✅ Updated to compatible package versions
- ✅ Removed redundant dependencies

### 2. Import Statement Corrections  
- ✅ Fixed `pypdf2` → `pypdf` import
- ✅ Corrected `from crewai import Agent` capitalization
- ✅ Fixed `from crewai_tools import SerperDevTool` import path
- ✅ Added proper `from crewai.tools import tool` decorator import

### 3. Tool Implementation Issues
- ✅ Made BloodTestReportTool inherit from BaseTool
- ✅ Added required attributes (name, description) to tool class
- ✅ Changed method name to `_run` (BaseTool requirement)
- ✅ Created proper tool instance for task usage
- ✅ Fixed tool decorator syntax: `@tool("Tool Name")`

### 4. Agent Optimization
- ✅ Replaced unprofessional agent descriptions with medical expertise
- ✅ Added ethical guidelines for medical analysis
- ✅ Reduced token usage with shorter backstories
- ✅ Added max_tokens=1000 limit to LLM
- ✅ Disabled memory and delegation to reduce complexity

### 5. Task Description Problems
- ✅ Removed tasks encouraging fabricated medical information
- ✅ Created evidence-based medical analysis tasks
- ✅ Streamlined descriptions to reduce token consumption
- ✅ Added proper clinical guidelines

### 6. Error Handling Enhancement
- ✅ Added comprehensive error handling throughout
- ✅ Implemented retry logic with exponential backoff
- ✅ Added file size validation (10MB limit)
- ✅ Added query length limits (200 characters)
- ✅ Improved error messages for user feedback

### 7. Token Limit Optimization
- ✅ Limited PDF content extraction to 3000 characters
- ✅ Added content truncation with messaging
- ✅ Optimized prompt engineering for efficiency
- ✅ Removed verbose logging output

### 8. API Improvements
- ✅ Enhanced FastAPI endpoint validation
- ✅ Implemented automatic file cleanup
- ✅ Added health check endpoint
- ✅ Removed uvicorn reload warnings

## 🏗️ Architecture

 
blood-test-analyzer/
├── main.py           # FastAPI server with endpoints
├── agents.py         # Medical analysis AI agents  
├── tasks.py          # CrewAI task definitions
├── tools.py          # PDF processing tools
├── requirements.txt  # Dependencies
└── .env             # API keys
 

 Components: 
-  FastAPI : RESTful API interface
-  CrewAI Agents : AI medical analysis agents
-  Groq LLM : Llama-3.3-70B for medical interpretation
-  PDF Tools : Extract and parse blood reports

## 🛠️ Setup Instructions

### 1. Install Dependencies
 bash
git clone <repository-url>
cd blood-test-analyzer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
 

### 2. Configure Environment
Create `.env` file:
 env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
 

### 3. Run Application
 bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
 
Server runs on `http://localhost:8000`

 Interactive API Documentation: `http://localhost:8000/docs`

## 📚 API Usage

### Health Check
 http
GET /
 

### Analyze Blood Report
 http
POST /analyze
 
 Parameters: 
- `file`: PDF blood test report
- `query`: Analysis question (optional)

 Example: 
 bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@blood_report.pdf" \
  -F "query=What are the abnormal values?"
 

 Response: 
 json
{
  "status": "success",
  "analysis": "Medical analysis results...",
  "file_processed": "blood_report.pdf"
}
 