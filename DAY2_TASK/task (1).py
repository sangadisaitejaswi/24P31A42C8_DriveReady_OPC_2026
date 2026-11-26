"""
Day 2 - AI Student Study Planner
Uses the Groq Python SDK directly (without LangChain).

Install: pip install groq
Set GROQ_API_KEY as an environment variable before running.
Never paste your API key into this file or upload it to GitHub.
"""
import os
from groq import Groq


def get_student_details():
    print("\n===== AI STUDENT STUDY PLANNER =====\n")
    name = input("Enter your name: ").strip()
    subjects = input("Enter your subjects (comma-separated): ").strip()
    difficult_topics = input("Enter topics you find difficult (comma-separated): ").strip()
    exam_date = input("Enter your exam date (for example, 15 December 2026): ").strip()
    study_hours = input("How many hours can you study per day? ").strip()
    return name, subjects, difficult_topics, exam_date, study_hours


def generate_study_plan(name, subjects, difficult_topics, exam_date, study_hours):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY was not found. Add it to your environment or Colab Secrets.")

    client = Groq(api_key=api_key)
    prompt = f"""
Create a realistic exam preparation plan using these details:
Student name: {name}
Subjects: {subjects}
Difficult topics: {difficult_topics}
Exam date: {exam_date}
Available study time per day: {study_hours} hours

Include:
1. A short preparation strategy.
2. A day-wise study timetable leading up to the exam.
3. Extra practice time for difficult topics.
4. Short breaks and revision sessions.
5. A final revision checklist.

Keep the plan realistic. If details are unclear, mention the uncertainty.
Do not invent the student's syllabus or claim to know the exam question paper.
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You create clear, realistic and encouraging study plans."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content


def main():
    try:
        details = get_student_details()
        plan = generate_study_plan(*details)
        print("\n===== YOUR PERSONALIZED STUDY PLAN =====\n")
        print(plan)
        with open("study_plan.txt", "w", encoding="utf-8") as file:
            file.write(plan)
        print("\nYour study plan was saved to study_plan.txt.")
    except ValueError as error:
        print(f"Configuration error: {error}")
    except Exception as error:
        print(f"Something went wrong: {error}")
        print("Check your Groq API key, internet connection, and model access.")


if __name__ == "__main__":
    main()
