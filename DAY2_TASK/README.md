# Day 2 - AI Student Study Planner

## Project Description
A Python application that uses the **Groq API directly through the Groq Python SDK, without LangChain**, to generate a personalized exam preparation plan.

The student enters their subjects, difficult topics, exam date, and available study hours. The application sends these details to a Groq-hosted language model and displays a suggested study plan.

## Objectives
- Connect a Python program to an LLM provider using its Python SDK.
- Send messages to a chat-completion model and receive a response.
- Use user input to generate a personalized result.
- Practice secure API-key handling and error handling.

## Technologies Used
- Python
- Groq Python SDK
- Groq API
- Google Colab or a local Python environment

## Features
1. Accepts the student's name and subjects.
2. Collects difficult topics, exam date, and daily study hours.
3. Generates a day-wise study timetable.
4. Includes revision sessions and breaks.
5. Saves the generated plan in `study_plan.txt`.

## Installation
```bash
pip install groq
```

## API Key Setup
Create or use a Groq API key from https://console.groq.com/keys.

Set it as an environment variable named `GROQ_API_KEY`.

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY="your_api_key"
```

**macOS/Linux:**
```bash
export GROQ_API_KEY="your_api_key"
```

**Google Colab:**
1. Open the Secrets panel (key icon).
2. Add a secret named `GROQ_API_KEY`.
3. Paste your Groq API key as its value.
4. Turn Notebook access ON.

Then run:
```python
from google.colab import userdata
import os

os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
```

Never write your real API key in `task.py`, `README.md`, notebook outputs, or a public GitHub repository.

## How to Run
```bash
python task.py
```

Enter the requested details when prompted. The generated study plan will be displayed and saved to `study_plan.txt`.

## How It Works
1. The program collects student details using Python `input()`.
2. The Groq client reads the API key from the environment.
3. The program sends a system message and the student's details to the Groq API.
4. The model generates a personalized study plan.
5. The program prints the result and saves it to a text file.

## Learning Outcome
This task demonstrates how to call a language model directly using the Groq Python SDK, without using LangChain.
