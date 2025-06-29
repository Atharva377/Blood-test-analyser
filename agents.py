import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import search_tool, blood_test_report_tool
from langchain_groq import ChatGroq

# Improved LLM configuration
llm = ChatGroq(
    temperature=0.1,  # Very low temperature for consistent medical analysis
    model_name="groq/llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    request_timeout=60,  # Increased timeout
    max_retries=3,
    stop_sequences=["</analysis>", "END_RESPONSE"]  # Add stop sequences
)

# Simplified, focused doctor agent
doctor = Agent(
    role="Medical Report Analyst",
    goal="Analyze blood test reports and provide clear, concise medical insights",
    backstory=(
        "You are a medical professional specializing in blood test interpretation. "
        "You provide accurate, evidence-based analysis of lab results. "
        "You always structure your responses clearly and keep them concise. "
        "When analyzing blood tests, you focus on key abnormal values and their clinical significance."
    ),
    verbose=True,
    memory=False,
    max_iter=2,  # Reduced iterations
    max_rpm=5,
    llm=llm,
    allow_delegation=False,  # Prevent delegation issues
    system_template="""You are a medical analyst. When analyzing blood reports:
1. First read the document content carefully
2. Identify key abnormal values
3. Provide brief clinical interpretation
4. Keep response under 500 words
5. Always end with "END_RESPONSE" when complete"""
)