# Confucius Calendar

A smart task scheduler that uses generative AI to help you manage your tasks wisely.

## For Users (Running the Executable)

If you have downloaded the executable version of Confucius Calendar, you do not need to install Python or any modules. The only setup step is to provide your own API key for the generative AI service.

### 1. Set Up Your API Key

This application uses the Google Gemini API to generate task durations and schedules. You will need to get your own API key from Google AI Studio.

1.  Go to [Google AI Studio](https://aistudio.google.com/) and create an API key.
2.  Set the API key as an environment variable named `GEMINI_API_KEY`.

**On Windows:**

You can set the environment variable using the command prompt:
```bash
setx GEMINI_API_KEY "YOUR_API_KEY"
```
**Important:** After running this command, you must **restart your computer** for the change to take effect.

### 2. Run the Application

After setting up your API key, you can run the application by double-clicking the `gui.exe` file (or `gui` on macOS) in your file explorer.

---

## For Developers (Running from Source)

If you want to run the application from the source code or contribute to the project, follow these instructions.

### 1. Prerequisites

- Python 3.x
- Git

### 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd Confucius-Calendar
```

### 3. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage the project's dependencies.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 4. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 5. Set Up Your API Key

This application uses the Google Gemini API. You will need to get your own API key from Google AI Studio.

1.  Go to [Google AI Studio](https://aistudio.google.com/) and create an API key.
2.  Set the API key as an environment variable named `GEMINI_API_KEY`.

**On Windows:**

```bash
setx GEMINI_API_KEY "YOUR_API_KEY"
```

**On macOS/Linux:**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

**Note:** You may need to restart your terminal or your computer for the environment variable to be recognized.

### 6. How to Run the Application

Once you have completed the setup steps, you can run the application with the following command:

```bash
python gui.py
```