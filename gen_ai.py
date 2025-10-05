import os
import google.generativeai as genai

def get_gemini_model():
    """Initializes and returns the Gemini generative model."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Set GEMINI_API_KEY environment variable first.")
    genai.configure(api_key=key)
    model = genai.GenerativeModel("models/gemini-flash-latest")
    return model

def get_task_duration(task_name, due_date):
    """Gets the task duration from the Gemini API."""
    model = get_gemini_model()
    prompt = f"Given the task '{task_name}' with a due date of {due_date}, how many hours should be allocated for this task? Please provide only the number of hours."
    response = model.generate_content(prompt)
    try:
        return int(response.text.strip())
    except ValueError:
        # Handle cases where the model doesn't return a valid number
        return 1 # Default to 1 hour if parsing fails

def generate_schedule(tasks):
    """Generates a schedule using the Gemini API based on the provided tasks."""
    model = get_gemini_model()
    
    prompt = f"""
    Here is a list of tasks: {tasks}.
    
    Generate a schedule for these tasks with the following considerations:
    1. Schedule tasks between 8:00 AM and 8:00 PM.
    2. For every 2 hours of a task, add a 15-minute break. Breaks should be explicitly listed.
    3. If a task's duration is long, spread it across multiple days before the due date.
    4. Prioritize scheduling tasks as close to their due date as possible, but ensure they are completed before the due date.
    5. Multiple tasks can be scheduled in one day if their total duration is not too long.
    6. Ensure all parts of a task are scheduled before its due date.
    7. Each task must be completed within 3 days before the deadline.
    8. Each task should start within a month before the due date.
    
    Provide the output as a JSON object where each key is a date (YYYY-MM-DD) and the value is a list of events for that day. 
    Each event in the list should be a dictionary with 'name', 'start_time', and 'end_time'. For tasks, the name should be the task name. For breaks, the name should be 'Break'.
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    model = get_gemini_model()
    resp = model.generate_content("Say: Gemini is connected.")
    print(resp.text)
