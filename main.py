from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import time
from crewai import Crew, Process
from agents import doctor
from task import help_patients

app = FastAPI(title="Blood Test Report Analyser")


def run_crew(query: str, file_path: str) -> str:
    try:
        # Add timeout and error handling
        medical_crew = Crew(
            agents=[doctor],
            tasks=[help_patients],
            process=Process.sequential,
            verbose=True,  # Enable verbose for debugging
            memory=False,
            max_execution_time=120  # 2 minutes timeout
        )
        
        result = medical_crew.kickoff(
            inputs={
                'query': query,
                'path': file_path
            }
        )
        
        # Better result handling
        if result and hasattr(result, 'raw'):
            return str(result.raw)[:1000]
        elif result:
            return str(result)[:1000]
        else:
            return "Analysis completed but no specific recommendations generated."
            
    except Exception as e:
        error_msg = str(e)
        if "RateLimitError" in error_msg or "rate limit" in error_msg.lower():
            return "Our medical analysis service is currently busy. Please try again in a few minutes."
        elif "timeout" in error_msg.lower() or "Maximum iterations" in error_msg:
            return "Analysis took longer than expected. Please try with a shorter query or smaller file."
        else:
            return f"Error processing request: {error_msg[:200]}"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a brief summary of this blood test report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Provide a brief summary of this blood test report"
        
        # Limit query length to prevent issues
        query = query.strip()[:200]
            
        # Process the blood report
        response = run_crew(query=query, file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)[:200]}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)