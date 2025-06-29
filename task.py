from crewai import Task
from agents import doctor
from tools import blood_test_report_tool

help_patients = Task(
    description="""
    1. Use the blood_test_report_tool to read the file at {path}
    2. Analyze the blood test results for the query: {query}
    3. Provide a clear, structured response focusing on:
       - Key abnormal values found
       - Clinical interpretation
       - Basic recommendations
    4. Keep response under 400 words
    5. End with "END_RESPONSE"
    """,
    expected_output="""
    A structured analysis containing:
    - Summary of key findings
    - Abnormal values and their significance
    - General health recommendations
    - Response ending with "END_RESPONSE"
    """,
    agent=doctor,
    tools=[blood_test_report_tool],
    async_execution=False,
    max_execution_time=90,  # 90 second timeout per task
)