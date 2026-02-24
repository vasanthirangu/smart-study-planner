from google import genai
import os
import time

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

PRIMARY_MODEL = "gemini-flash-latest"
FALLBACK_MODEL = "gemini-flash-lite-latest"


def generate_with_retry(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=PRIMARY_MODEL,
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(3)

    # Fallback model
    try:
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt
        )
        return response.text
    except Exception:
        return "⚠️ AI service temporarily unavailable. Please try again later."


def extract_topics_from_text(text):
    prompt = f"""
    Extract important study topics from the following syllabus content.
    Return as a clean bullet list.

    Content:
    {text}
    """
    return generate_with_retry(prompt)


def generate_ai_schedule(subject, topics, exam_date, hours_per_day):
    prompt = f"""
    Create a detailed study schedule.

    Subject: {subject}
    Topics: {topics}
    Exam date: {exam_date}
    Hours per day: {hours_per_day}

    Prioritize difficult topics first.
    Include revision days.
    Make it structured day-wise.
    """
    return generate_with_retry(prompt)